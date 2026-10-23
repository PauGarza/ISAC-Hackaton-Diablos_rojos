"""Paso 5: scores por pitch, pitcher y arsenal (entorno nativo, nivel del mar y Harp Helú), delta de
altitud por forma de pitch (clusters), pruebas H2/H3, estabilidad, mapas de ubicación y equipo Diablos."""
import os, json
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from comun import *
from stuffplus import ModeloStuff, trasladar

M = ModeloStuff()
d = pd.read_parquet(os.path.join(TRABAJO, "pitches.parquet")).merge(
    pd.read_parquet(os.path.join(TRABAJO, "contacto.parquet")), on="fila")
R = RESULTADOS

# ---------- Scores por pitcheo ----------
for fs, nom in [("stuff", "stuff"), ("loc", "location"), ("pitch", "pitching")]:
    p = M.predecir(d, fs)
    d[f"xrv_{nom}"] = p["xrv"].to_numpy(); d[f"{nom}_plus"] = p["plus"].to_numpy()
    if fs == "stuff":
        for c in ["p_whiff", "p_called_strike", "p_bip", "p_gb", "p_hard", "p_out_bip"]:
            d[f"stuff_{c}"] = p[c].to_numpy()
    if fs == "pitch":
        d["pitch_p_swing"] = (p["p_whiff"] + p["p_foul"] + p["p_bip"]).to_numpy()
        d["pitch_p_whiff"] = p["p_whiff"].to_numpy()
        d["pitch_p_called"] = p["p_called_strike"].to_numpy()
for alt, suf in [(ALT_NIVEL_MAR, "mar"), (ALT_HARP_HELU, "hh")]:
    t = trasladar(d, alt, M.k)
    d[f"ivb_{suf}"] = t["InducedVertBreak"].to_numpy(); d[f"hb_{suf}"] = t["hb_m"].to_numpy()
    for fs, nom in [("stuff", "stuff"), ("pitch", "pitching")]:
        p = M.predecir(t, fs)
        d[f"xrv_{nom}_{suf}"] = p["xrv"].to_numpy(); d[f"{nom}_plus_{suf}"] = p["plus"].to_numpy()
    del t
d["delta_stuff_hh"] = d["stuff_plus_hh"] - d["stuff_plus_mar"]
d["delta_pitching_hh"] = d["pitching_plus_hh"] - d["pitching_plus_mar"]

# ---------- Clusters de forma (H4: forma sobre etiqueta), sobre movimiento a nivel del mar ----------
cf = ["RelSpeed", "ivb_mar", "hb_mar", "SpinRate", "velo_diff"]
Z = StandardScaler().fit_transform(d[cf].fillna(d[cf].median()))
km = KMeans(n_clusters=14, n_init=4, random_state=0).fit(Z[::5])
d["forma"] = km.predict(Z)
desc = d.groupby("forma").agg(tipo_dominante=("AutoPitchType", lambda s: s.value_counts().index[0]),
                              pct_tipo=("AutoPitchType", lambda s: round(100 * s.value_counts(normalize=True).iat[0])),
                              velo=("RelSpeed", "mean"), ivb_mar=("ivb_mar", "mean"), hb_mar=("hb_mar", "mean"),
                              spin=("SpinRate", "mean"), n=("fila", "size"))


def nombre_forma(r):
    hb = "brazo" if r.hb_mar > 4 else ("guante" if r.hb_mar < -4 else "recto")
    v = "ride" if r.ivb_mar > 15 else ("caída" if r.ivb_mar < 0 else "medio")
    return f"{r.tipo_dominante} {r.velo:.0f}mph IVB{r.ivb_mar:+.0f} HB{r.hb_mar:+.0f} ({hb}, {v})"


desc["forma_nombre"] = [nombre_forma(r) for r in desc.itertuples()]
d["forma_nombre"] = d["forma"].map(desc["forma_nombre"])

ag = lambda g: g.agg(n=("fila", "size"), stuff_mar=("stuff_plus_mar", "mean"), stuff_hh=("stuff_plus_hh", "mean"),
                     delta_stuff=("delta_stuff_hh", "mean"), pitching_mar=("pitching_plus_mar", "mean"),
                     pitching_hh=("pitching_plus_hh", "mean"), delta_pitching=("delta_pitching_hh", "mean"),
                     ivb_mar=("ivb_mar", "mean"), ivb_hh=("ivb_hh", "mean"), hb_mar=("hb_mar", "mean"), hb_hh=("hb_hh", "mean"))
porforma = ag(d.groupby("forma_nombre")).round(2).sort_values("delta_stuff", ascending=False)
porforma.to_csv(os.path.join(R, "delta_altitud_por_forma.csv"))
portipo = ag(d.groupby("AutoPitchType")).round(2).sort_values("delta_stuff", ascending=False)
portipo.to_csv(os.path.join(R, "delta_altitud_por_tipo.csv"))
print(portipo.to_string()); print(porforma.to_string())

# ---------- H3: valor del contacto por tipo de batazo, mismo EV/LA, nivel del mar vs Harp Helú ----------
mc = lgb.Booster(model_file=os.path.join(MODELOS, "contacto_xrv.txt"))
b = d[(d["clase"] == "bip") & d["ExitSpeed"].notna() & d["Angle"].notna()]
h3 = []
for alt, suf in [(0, "mar"), (ALT_HARP_HELU, "hh")]:
    x = b[["ExitSpeed", "Angle"]].assign(altitude_m=alt)
    h3.append(pd.Series(mc.predict(x), index=b.index, name=suf))
h3 = pd.concat(h3, axis=1).assign(hit_type=b["hit_type"]).groupby("hit_type").agg(
    n=("mar", "size"), xrv_mar=("mar", "mean"), xrv_hh=("hh", "mean"))
h3["delta"] = h3["xrv_hh"] - h3["xrv_mar"]
h3.round(3).to_csv(os.path.join(R, "h3_valor_contacto_por_batazo.csv")); print(h3.round(3))
# observado por categoría
obs = d[d["clase"] == "bip"].groupby(["altitude_category", "hit_type"])["valor_evento"].agg(["size", "mean"]).round(3)
obs.to_csv(os.path.join(R, "h3_valor_observado_por_batazo_y_altitud.csv"))

# ---------- Agregados por pitcher y arsenal ----------
def agrega(g):
    return g.agg(n=("fila", "size"), equipo=("equipo_pitcher", lambda s: s.mode().iat[0] if s.notna().any() else None),
                 mano=("PitcherThrows", "first"),
                 xrv_stuff=("xrv_stuff", "mean"), xrv_location=("xrv_location", "mean"), xrv_pitching=("xrv_pitching", "mean"),
                 xrv_stuff_mar=("xrv_stuff_mar", "mean"), xrv_stuff_hh=("xrv_stuff_hh", "mean"),
                 xrv_pitching_mar=("xrv_pitching_mar", "mean"), xrv_pitching_hh=("xrv_pitching_hh", "mean"),
                 rv100=("rv_obs", lambda s: 100 * s.mean()), velo=("RelSpeed", "mean"),
                 ivb=("ivb", "mean"), hb=("hb_m", "mean"), spin=("SpinRate", "mean"),
                 whiff_swing=("clase", lambda s: (s == "whiff").sum() / max(1, s.isin(["whiff", "foul", "bip"]).sum())),
                 gb_bip=("gb", "mean"), hard_bip=("hard", "mean"), p_gb_modelo=("stuff_p_gb", "mean"))


def escalar(t, minimo, ref=None):
    """Re-escala a nivel agregado: 100 + 10 z con media/sd de los calificados (entorno nativo)."""
    ref = ref if ref is not None else t[t["n"] >= minimo]
    for nom in ["stuff", "location", "pitching"]:
        mu, sd = np.average(ref[f"xrv_{nom}"], weights=ref["n"]), ref[f"xrv_{nom}"].std()
        cols = [c for c in t if c.startswith(f"xrv_{nom}")]
        for c in cols:
            t[c.replace("xrv_", "") .replace(nom, nom + "_plus", 1)] = escala_plus(t[c], mu, sd)
    t["delta_stuff_hh"] = t["stuff_plus_hh"] - t["stuff_plus_mar"]
    t["delta_pitching_hh"] = t["pitching_plus_hh"] - t["pitching_plus_mar"]
    return t


pit = escalar(agrega(d.groupby("pitcher_anon_id")).reset_index(), 300)
pit_y = escalar(agrega(d.groupby(["pitcher_anon_id", "year"])).reset_index(), 200)
ars = escalar(agrega(d.groupby(["pitcher_anon_id", "AutoPitchType"])).reset_index(), 75)
uso = d.groupby("pitcher_anon_id").size()
ars["uso_%"] = 100 * ars["n"] / ars["pitcher_anon_id"].map(uso)
pit.round(3).to_csv(os.path.join(R, "scores_pitcher.csv"), index=False)
pit_y.round(3).to_csv(os.path.join(R, "scores_pitcher_temporada.csv"), index=False)
ars.round(3).to_csv(os.path.join(R, "scores_arsenal.csv"), index=False)

# Estabilidad y poder predictivo (pitcher-temporada, >=200 pitcheos)
q = pit_y[pit_y["n"] >= 200].pivot(index="pitcher_anon_id", columns="year")
est = []
for a, b_ in [(2024, 2025), (2025, 2026)]:
    for col in ["stuff_plus", "location_plus", "pitching_plus", "rv100"]:
        x = q[[(col, a), ("rv100", b_), (col, b_)]].dropna()
        est.append({"de": a, "a": b_, "metrica": col, "n": len(x),
                    "r_mismo_metrica_año_sig": round(x[[(col, a), (col, b_)]].corr().iat[0, 1], 3),
                    "r_vs_rv100_año_sig": round(x[[(col, a), ("rv100", b_)]].corr().iat[0, 1], 3) * (-1 if col != "rv100" else 1)})
pd.DataFrame(est).to_csv(os.path.join(R, "estabilidad_y_prediccion.csv"), index=False); print(pd.DataFrame(est))

# ---------- Mapas de ubicación: Pitching+ por zona, Harp Helú vs nivel del mar, por grupo de pitch ----------
z = d[d["PlateLocHeight"].notna()].copy()
z["alto"] = pd.cut(z["PlateLocHeight"], [-9, 1.62, 2.15, 2.68, 3.21, 9], labels=["bajo fuera", "bajo", "medio", "alto", "alto fuera"])
z["lado"] = pd.cut(z["PlateLocSide_m"], [-9, -0.708, -0.236, 0.236, 0.708, 9], labels=["guante fuera", "guante", "centro", "brazo", "brazo fuera"])
mapa = z.groupby(["grupo", "alto", "lado"], observed=True).agg(n=("fila", "size"), pitching_mar=("pitching_plus_mar", "mean"),
                                                              pitching_hh=("pitching_plus_hh", "mean"), location=("location_plus", "mean"))
mapa["delta_hh"] = mapa["pitching_hh"] - mapa["pitching_mar"]
mapa.round(2).to_csv(os.path.join(R, "mapa_ubicacion_por_grupo.csv"))

# ---------- Diablos ----------
dia = d[d["equipo_pitcher"] == "Diablos"]
ids = dia.groupby("pitcher_anon_id").size()
ids = ids[ids >= 150].index
casa = d[(d["pitcher_anon_id"].isin(ids))]
casa = casa.assign(sede=np.where(casa["harp_helu"] == 1, "Harp Helú", "visita"))
split = casa.groupby(["pitcher_anon_id", "sede"]).agg(n=("fila", "size"), rv100=("rv_obs", lambda s: 100 * s.mean()),
                                                    stuff=("stuff_plus", "mean"), pitching=("pitching_plus", "mean")).unstack()
split.round(2).to_csv(os.path.join(R, "diablos_casa_vs_visita.csv"))
pit[pit["pitcher_anon_id"].isin(ids)].sort_values("stuff_plus_hh", ascending=False).round(2).to_csv(os.path.join(R, "diablos_pitchers.csv"), index=False)
ars[ars["pitcher_anon_id"].isin(ids) & (ars["n"] >= 40)].sort_values(["pitcher_anon_id", "stuff_plus_hh"], ascending=[True, False]).round(2).to_csv(os.path.join(R, "diablos_arsenal.csv"), index=False)
mix = d[d["pitcher_anon_id"].isin(ids)].assign(sede=lambda x: np.where(x["harp_helu"] == 1, "Harp Helú", "visita")).groupby(["sede", "AutoPitchType"]).size().unstack(0)
(100 * mix / mix.sum()).round(1).to_csv(os.path.join(R, "diablos_mezcla_casa_vs_visita.csv"))

# ---------- Salida por pitcheo (para simulador / documento) ----------
cols = ["PitchUID", "game_anon_id", "pitcher_anon_id", "year", "equipo_pitcher", "estadio", "altitude_m", "harp_helu",
        "PitcherThrows", "BatterSide", "AutoPitchType", "forma_nombre", "RelSpeed", "SpinRate", "SpinAxis", "InducedVertBreak", "HorzBreak",
        "ivb_mar", "hb_mar", "ivb_hh", "hb_hh", "PlateLocSide", "PlateLocHeight", "count_k", "clase", "rv_obs",
        "xrv_stuff", "stuff_plus", "xrv_location", "location_plus", "xrv_pitching", "pitching_plus",
        "stuff_plus_mar", "stuff_plus_hh", "delta_stuff_hh", "pitching_plus_mar", "pitching_plus_hh", "delta_pitching_hh",
        "stuff_p_whiff", "stuff_p_called_strike", "stuff_p_gb", "stuff_p_hard", "stuff_p_out_bip", "pitch_p_swing", "pitch_p_whiff", "pitch_p_called"]
d[cols].to_parquet(os.path.join(R, "scores_pitch.parquet"), index=False)
desc.to_csv(os.path.join(R, "formas_clusters.csv"))
print("listo")
