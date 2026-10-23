"""Paso 1: limpieza, unión con estadios, reconstrucción de PA, valores de carrera por count,
features de arsenal. Salida: intermedios/pitches.parquet + resultados/tablas de run value."""
import os, json
import numpy as np
import pandas as pd
from comun import *

os.makedirs(TRABAJO, exist_ok=True); os.makedirs(RESULTADOS, exist_ok=True)
d = pd.read_parquet(DATOS)
d["fila"] = np.arange(len(d))
n0 = len(d)

# --- Limpieza (propuesta §2) ---
d["EffectiveVelo"] = pd.to_numeric(d["EffectiveVelo"], errors="coerce")
for c in ["PitchCall", "AutoPitchType", "Top/Bottom", "play_result"]:
    d[c] = d[c].astype(str)
d.loc[d["PlateLocHeight"] == 0, "PlateLocHeight"] = np.nan
d["is_hit_by_pitch"] = (d["PitchCall"] == "HitByPitch").astype(int)
# Manos: imputar por moda del jugador; switch -> lado opuesto al pitcher
for col, idc in [("PitcherThrows", "pitcher_anon_id"), ("BatterSide", "batter_anon_id")]:
    ok = d[col].isin(["Right", "Left"])
    moda = d[ok].groupby(idc)[col].agg(lambda s: s.mode().iat[0])
    d.loc[~ok, col] = d.loc[~ok, idc].map(moda)
sw = ~d["BatterSide"].isin(["Right", "Left"])
d.loc[sw, "BatterSide"] = np.where(d.loc[sw, "PitcherThrows"] == "Right", "Left", "Right")
d["AutoPitchType"] = d["AutoPitchType"].replace({"OneSeamFastBall": "Other", "TwoSeamFastBall": "Sinker", "Knuckleball": "Other"})

# --- Estadio / altitud continua ---
j = pd.read_csv(JUEGOS)
d = d.merge(j[["game_anon_id", "home_team", "away_team", "home_equipo", "away_equipo", "estadio", "altitud_m", "harp_helu"]],
            on="game_anon_id", how="left")
d = d.sort_values("fila").reset_index(drop=True)
d["altitude_m"] = d["altitud_m"]
d["equipo_pitcher"] = np.where(d["Top/Bottom"] == "Top", d["home_equipo"], d["away_equipo"])
d["equipo_bateador"] = np.where(d["Top/Bottom"] == "Top", d["away_equipo"], d["home_equipo"])

# --- PA, número de pitcheo, bateadores enfrentados (orden de filas secuencial por juego) ---
term = (d["KorBB"].isin(["Strikeout", "Walk"]) | (d["PitchCall"].isin(["InPlay", "HitByPitch"]))).to_numpy()
d["fin_pa"] = term.astype(np.int8)
g = d.groupby("game_anon_id", sort=False)
d["pa_id"] = g["fin_pa"].transform(lambda s: s.shift(fill_value=0).cumsum())
d["pa_key"] = d["game_anon_id"] + "_" + d["pa_id"].astype(str)
d["n_pitch_juego"] = d.groupby(["game_anon_id", "pitcher_anon_id"]).cumcount() + 1
first = ~d.duplicated("pa_key")
d["bat_enfrentados"] = first.astype(int).groupby([d["game_anon_id"], d["pitcher_anon_id"]]).cumsum()

# --- Valor de carrera de eventos (RE por outs; corredores marginalizados) ---
d["media_entrada"] = d["game_anon_id"] + "_" + d["Inning"].astype(str) + "_" + d["Top/Bottom"]
rs = d["RunsScored"].fillna(0)
d["runs_rest"] = rs[::-1].groupby(d["media_entrada"][::-1]).cumsum()[::-1]  # carreras desde este pitcheo al fin de la media entrada
pa = d[first][["pa_key", "Outs", "runs_rest", "media_entrada", "Inning"]].copy()
# solo medias entradas completas (3 outs) y entradas 1-8, para no truncar
outs_me = d.groupby("media_entrada")["OutsOnPlay"].sum()
completas = outs_me[outs_me >= 3].index
pa = pa[pa["media_entrada"].isin(completas) & (pa["Inning"] <= 8)]
re_outs = pa.groupby("Outs")["runs_rest"].mean()
ultimo = d[d["fin_pa"] == 1][["pa_key", "PitchCall", "KorBB", "play_result"]]


def evento(r):
    if r.KorBB == "Strikeout": return "K"
    if r.KorBB == "Walk": return "BB"
    if r.PitchCall == "HitByPitch": return "HBP"
    pr = r.play_result
    return {"Single": "1B", "Double": "2B", "Triple": "3B", "HomeRun": "HR", "Error": "E",
            "FieldersChoice": "OUT", "Sacrifice": "OUT", "Out": "OUT"}.get(pr, "OUT")


ultimo = ultimo.assign(evento=[evento(r) for r in ultimo.itertuples()])
pa = pa.merge(ultimo[["pa_key", "evento"]], on="pa_key")
pa["valor"] = pa["runs_rest"] - pa["Outs"].map(re_outs)
lw = pa.groupby("evento")["valor"].mean()
lw = lw - (pa["valor"].mean())  # centrar en PA promedio
print("RE por outs:", re_outs.round(3).to_dict()); print("Pesos lineales LMB:", lw.round(3).to_dict())

# Valor de cada count = valor medio del evento final de las PA que pasan por ese count
d = d.merge(ultimo[["pa_key", "evento"]], on="pa_key", how="left")
d = d.sort_values("fila").reset_index(drop=True)
d["valor_evento"] = d["evento"].map(lw)
d["count_k"] = d["Balls"].clip(0, 3).astype("Int64").astype(str) + "-" + d["Strikes"].clip(0, 2).astype("Int64").astype(str)
pc = d.dropna(subset=["valor_evento"]).drop_duplicates(["pa_key", "count_k"])
v_count = pc.groupby("count_k")["valor_evento"].mean()
print("Valor por count:", v_count.round(3).to_dict())

# --- Clase de desenlace y run value observado por pitcheo ---
pcall = d["PitchCall"]
cl = np.select(
    [pcall.isin(["BallCalled", "BallinDirt", "BallIntentional", "AutomaticBall"]),
     pcall.isin(["StrikeCalled", "AutomaticStrike"]), pcall == "StrikeSwinging",
     pcall.isin(["FoulBallNotFieldable", "FoulBall", "FoulBallFieldable"]),
     pcall == "InPlay", pcall == "HitByPitch"],
    CLASES, default="undef")
d["clase"] = cl


def rv_transicion(balls, strikes, clase, v):
    """Run value (carreras, + bateador) de pasar del count actual al siguiente, por clase. bip -> NaN."""
    b, s = int(balls), int(strikes)
    vc = v[f"{b}-{s}"]
    if clase == "ball": return (lw["BB"] if b == 3 else v[f"{b+1}-{s}"]) - vc
    if clase in ("called_strike", "whiff"): return (lw["K"] if s == 2 else v[f"{b}-{s+1}"]) - vc
    if clase == "foul": return 0.0 if s == 2 else v[f"{b}-{s+1}"] - vc
    if clase == "hbp": return lw["HBP"] - vc
    return np.nan


tabla = {}
for b in range(4):
    for s in range(3):
        for c in CLASES:
            tabla[(b, s, c)] = rv_transicion(b, s, c, v_count)
bb = d["Balls"].clip(0, 3).fillna(0).astype(int); ss = d["Strikes"].clip(0, 2).fillna(0).astype(int)
d["rv_obs"] = [tabla.get((b, s, c), np.nan) for b, s, c in zip(bb, ss, d["clase"])]
bip = d["clase"] == "bip"
d.loc[bip, "rv_obs"] = d.loc[bip, "valor_evento"] - d.loc[bip, "count_k"].map(v_count)
d["v_count"] = d["count_k"].map(v_count)

# Banderas de contacto
d["gb"] = (d["hit_type"] == "GroundBall").astype(float).where(bip)
d["hard"] = (d["ExitSpeed"] >= 95).astype(float).where(bip & d["ExitSpeed"].notna())
d["weak"] = (d["ExitSpeed"] < 80).astype(float).where(bip & d["ExitSpeed"].notna())
d["out_bip"] = d["evento"].isin(["OUT"]).astype(float).where(bip)
d["barrel"] = ((d["ExitSpeed"] >= 98) & d["Angle"].between(26 - (d["ExitSpeed"] - 98), 30 + 1.2 * (d["ExitSpeed"] - 98))).astype(float).where(bip & d["ExitSpeed"].notna())
d["in_zone"] = d["in_strike_zone"]
d["swing"] = d["clase"].isin(["whiff", "foul", "bip"]).astype(int)

# --- Filtros físicos ---
ok = (d["RelSpeed"].between(60, 105) & d["Extension"].between(3, 8.5) & d["SpinRate"].notna()
      & d["InducedVertBreak"].notna() & d["HorzBreak"].notna() & d["altitude_m"].notna()
      & (d["clase"] != "undef") & ~d["AutoPitchType"].isin(["Other", "nan"]))
print(f"Filas: {n0} -> {ok.sum()} tras filtros")
d = d[ok].copy()

# --- Fastball primaria por pitcher-temporada y referencia por entorno (categoría de altitud) ---
fb = d[d["AutoPitchType"].isin(TIPOS_FB)]
prim = fb.groupby(["pitcher_anon_id", "year"])["AutoPitchType"].agg(lambda s: s.value_counts().index[0]).rename("fb_tipo")
d = d.merge(prim, on=["pitcher_anon_id", "year"], how="left")
d = d.sort_values("fila").reset_index(drop=True)
# Pitchers sin fastball: usar su pitch más rápido
sin = d["fb_tipo"].isna()
if sin.any():
    rapido = d[sin].groupby(["pitcher_anon_id", "year", "AutoPitchType"])["RelSpeed"].mean().reset_index()
    rapido = rapido.sort_values("RelSpeed").groupby(["pitcher_anon_id", "year"]).tail(1).set_index(["pitcher_anon_id", "year"])["AutoPitchType"]
    d.loc[sin, "fb_tipo"] = pd.MultiIndex.from_frame(d.loc[sin, ["pitcher_anon_id", "year"]]).map(rapido)
d = construir_features(d)
esfb = d["AutoPitchType"] == d["fb_tipo"]
cols = {"RelSpeed": "fb_velo", "ivb": "fb_ivb", "hb_m": "fb_hb", "spin_axis_m": "fb_axis"}
for nivel in [["pitcher_anon_id", "year", "altitude_category"], ["pitcher_anon_id", "year"], ["pitcher_anon_id"]]:
    ref = d[esfb].groupby(nivel)[list(cols)].mean().rename(columns=cols)
    m = d[nivel].merge(ref, left_on=nivel, right_index=True, how="left")
    for c in cols.values():
        d[c] = d[c].fillna(m[c]) if c in d else m[c]
d = construir_features(d)

keep = (["fila", "PitchUID", "game_anon_id", "pitcher_anon_id", "batter_anon_id", "catcher_anon_id", "year",
         "PitcherThrows", "BatterSide", "AutoPitchType", "grupo", "fb_tipo", "altitude_category", "altitude_m",
         "estadio", "harp_helu", "home_equipo", "away_equipo", "equipo_pitcher", "equipo_bateador",
         "InducedVertBreak", "HorzBreak", "RelSide", "SpinAxis", "SpeedDrop", "VertApprAngle", "PlateLocSide",
         "fb_velo", "fb_ivb", "fb_hb", "fb_axis", "Inning", "Outs",
         "clase", "rv_obs", "v_count", "valor_evento", "evento", "count_k", "fin_pa", "pa_key",
         "gb", "hard", "weak", "barrel", "out_bip", "in_zone", "swing", "ExitSpeed", "Angle", "hit_type"]
        + FEATS_PITCH)
keep = list(dict.fromkeys(keep))
d[keep].to_parquet(os.path.join(TRABAJO, "pitches.parquet"), index=False)
json.dump({"re_outs": re_outs.to_dict(), "pesos_lineales": lw.to_dict(), "valor_count": v_count.to_dict(),
           "rv_transicion": {f"{b}-{s}|{c}": v for (b, s, c), v in tabla.items()}},
          open(os.path.join(MODELOS, "run_values.json"), "w"), indent=1, default=float)
print("ok", d.shape)
