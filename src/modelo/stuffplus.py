"""Librería de predicción: Stuff+ / Location+ / Pitching+ para cualquier pitch y estadio.

Uso típico (simulador):
    from stuffplus import ModeloStuff
    m = ModeloStuff()                       # carga los modelos de models/
    m.stuff_plus(dict(RelSpeed=95, SpinRate=2400, SpinAxis=210, RelHeight=6, RelSide=2, Extension=6.3,
                      InducedVertBreak=17, HorzBreak=8, PitcherThrows="Right", AutoPitchType="Four-Seam"),
                 altitud_destino=2240, altitud_medicion=0)
    m.comparar(pitch)  # Stuff+ al nivel del mar vs Harp Helú, con el movimiento trasladado

El movimiento (IVB/HB) que se pasa se interpreta como medido a `altitud_medicion` metros; se
traslada a `altitud_destino` con mov(alt) = mov(0) * exp(-k_tipo * alt_km) (ver k_altitud.json).
Si no se dan fb_velo/fb_ivb/fb_hb/fb_axis (fastball primaria del pitcher, medida a la misma
altitud), se usan los del propio pitch si es fastball, o una fastball típica de la liga.
"""
import os, json
import numpy as np
import pandas as pd
import lightgbm as lgb
from comun import MODELOS, CLASES, FEATS_STUFF, FEATS_LOC, FEATS_PITCH, construir_features, escala_plus, TIPOS_FB, ALT_HARP_HELU

FEATS = {"stuff": FEATS_STUFF, "loc": FEATS_LOC, "pitch": FEATS_PITCH}


def factor_altitud(k, tipo, comp, alt_desde, alt_hasta):
    kk = k.get(str(tipo), k["_global"]).get(comp, k["_global"][comp])
    return np.exp(-kk * (np.asarray(alt_hasta, float) - np.asarray(alt_desde, float)) / 1000.0)


def trasladar(df, alt_hasta, k, alt_desde_col="altitude_m"):
    """Devuelve copia de df con IVB/HB (y la fastball de referencia) trasladados a otra altitud."""
    out = df.copy()
    a0 = out[alt_desde_col].to_numpy(float)
    tipos = np.array([str(x) for x in out["AutoPitchType"].fillna("Four-Seam")], dtype=object)
    fbt = np.array([str(x) for x in out["fb_tipo"].fillna("Four-Seam")], dtype=object) if "fb_tipo" in out else tipos
    for comp, col, fbcol in [("ivb", "InducedVertBreak", "fb_ivb"), ("hb", "HorzBreak", "fb_hb")]:
        f = np.ones(len(out)); ffb = np.ones(len(out))
        for t in np.unique(tipos):
            sel = tipos == t
            f[sel] = factor_altitud(k, t, comp, a0[sel], alt_hasta)
        for t in np.unique(fbt):
            sel = fbt == t
            ffb[sel] = factor_altitud(k, t, comp, a0[sel], alt_hasta)
        out[col] = out[col] * f
        if fbcol in out:
            out[fbcol] = out[fbcol] * ffb
    out["altitude_m"] = alt_hasta
    return construir_features(out)


class ModeloStuff:
    def __init__(self, carpeta=MODELOS):
        self.k = json.load(open(os.path.join(carpeta, "k_altitud.json")))
        self.rv = json.load(open(os.path.join(carpeta, "run_values.json")))
        self.esc = json.load(open(os.path.join(carpeta, "escala.json")))
        self.fb_liga = self.esc["fb_liga"]
        self.m = {}
        for fs in FEATS:
            for h in ["clase", "bip_xrv", "gb", "hard", "out_bip"]:
                p = os.path.join(carpeta, f"{fs}_{h}.txt")
                if os.path.exists(p):
                    self.m[(fs, h)] = lgb.Booster(model_file=p)

    # ---------- núcleo vectorizado ----------
    def predecir(self, df, fs="stuff"):
        """df con features ya construidas. Devuelve DataFrame con probabilidades, xRV y escala plus."""
        X = df[FEATS[fs]].astype(float)
        P = self.m[(fs, "clase")].predict(X)
        out = pd.DataFrame(P, columns=[f"p_{c}" for c in CLASES], index=df.index)
        out["bip_xrv"] = self.m[(fs, "bip_xrv")].predict(X)
        for h in ["gb", "hard", "out_bip"]:
            if (fs, h) in self.m:
                out[f"p_{h}"] = self.m[(fs, h)].predict(X)
        if fs == "stuff":
            rvbar = self.esc["rv_medio_clase"]
            xrv = sum(out[f"p_{c}"] * rvbar[c] for c in CLASES if c != "bip")
            xrv += out["p_bip"] * (out["bip_xrv"] - self.esc["v_count_medio_bip"])
        else:
            b = df["Balls"].clip(0, 3).fillna(0).astype(int).astype(str)
            s = df["Strikes"].clip(0, 2).fillna(0).astype(int).astype(str)
            cnt = b + "-" + s
            tr = self.rv["rv_transicion"]
            xrv = 0.0
            for c in CLASES:
                if c == "bip":
                    continue
                xrv = xrv + out[f"p_{c}"] * (cnt + "|" + c).map(tr).astype(float)
            xrv = xrv + out["p_bip"] * (out["bip_xrv"] - cnt.map(self.rv["valor_count"]).astype(float))
        out["xrv"] = xrv
        e = self.esc[fs]
        out["plus"] = escala_plus(xrv, e["media"], e["sd"])
        return out

    # ---------- interfaz para el simulador ----------
    def _df_pitch(self, pitch, altitud_medicion):
        """Arma el DataFrame de un pitch. fb_hb y HB se dan en convención cruda de Trackman;
        internamente la fastball de referencia se guarda en espejo (zurdo -> diestro)."""
        p = dict(pitch)
        p.setdefault("BatterSide", "Right")
        p.setdefault("PitcherThrows", "Right")
        p.setdefault("AutoPitchType", "Four-Seam")
        tipo = str(p["AutoPitchType"])
        s = -1.0 if p["PitcherThrows"] == "Left" else 1.0
        df = pd.DataFrame([p])
        if "fb_velo" in p:  # fastball primaria del pitcher dada explícitamente
            df["fb_tipo"] = p.get("fb_tipo", "Four-Seam")
            df["fb_hb"] = p["fb_hb"] * s
            df["fb_axis"] = 360.0 - p["fb_axis"] if s < 0 else p["fb_axis"]
        elif tipo in TIPOS_FB:  # la fastball es su propia referencia
            df["fb_tipo"] = tipo
            df["fb_velo"], df["fb_ivb"] = p["RelSpeed"], p["InducedVertBreak"]
            df["fb_hb"] = p["HorzBreak"] * s
            df["fb_axis"] = 360.0 - p["SpinAxis"] if s < 0 else p["SpinAxis"]
        else:  # fastball típica de la liga (medida a nivel del mar) llevada a la altitud de medición
            fb = self.fb_liga
            df["fb_tipo"] = "Four-Seam"
            df["fb_velo"], df["fb_axis"] = fb["fb_velo"], fb["fb_axis"]
            df["fb_ivb"] = fb["fb_ivb"] * factor_altitud(self.k, "Four-Seam", "ivb", 0, altitud_medicion)
            df["fb_hb"] = fb["fb_hb"] * factor_altitud(self.k, "Four-Seam", "hb", 0, altitud_medicion)
        df["altitude_m"] = altitud_medicion
        return construir_features(df)

    def stuff_plus(self, pitch, altitud_destino=ALT_HARP_HELU, altitud_medicion=0.0, detalle=False):
        """Stuff+ de un pitch (dict de features físicas crudas de Trackman) en un estadio a `altitud_destino` m.
        Campos: RelSpeed, SpinRate, SpinAxis, RelHeight, RelSide, Extension, InducedVertBreak, HorzBreak,
        PitcherThrows, AutoPitchType; opcionales BatterSide y fb_velo/fb_ivb/fb_hb/fb_axis."""
        df = self._df_pitch(pitch, altitud_medicion)
        t = trasladar(df, altitud_destino, self.k)
        r = self.predecir(t, "stuff")
        if detalle:
            res = {k: float(v) for k, v in r.iloc[0].items()}
            res.update({"IVB_destino": float(t["InducedVertBreak"].iat[0]), "HB_destino": float(t["HorzBreak"].iat[0])})
            return res
        return float(r["plus"].iat[0])

    def comparar(self, pitch, altitud_medicion=0.0, altitudes=(0.0, ALT_HARP_HELU)):
        """Mismo pitch (misma mecánica de release) en varias altitudes."""
        return {a: self.stuff_plus(pitch, a, altitud_medicion, detalle=True) for a in altitudes}
