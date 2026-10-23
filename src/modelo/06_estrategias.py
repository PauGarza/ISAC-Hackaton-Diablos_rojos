"""Paso 6: insumos para las estrategias de Diablos en el Harp Helú.
- Ranking relativo por entorno: dónde quedaría cada pitcher si TODOS lanzaran en Harp Helú (o a nivel del mar).
- Rol (abridor/relevista) inferido por pitcheos por juego.
- Por pitcher de Diablos: qué pitch usar más / menos en casa (Stuff+ HH del pitch vs su promedio).
- Perfil: qué rasgos de forma pierden menos en altura (dentro de cada tipo)."""
import os
import numpy as np
import pandas as pd
from comun import *

R = RESULTADOS
pit = pd.read_csv(os.path.join(R, "scores_pitcher.csv"))
ars = pd.read_csv(os.path.join(R, "scores_arsenal.csv"))
sp = pd.read_parquet(os.path.join(R, "scores_pitch.parquet"))

# Rol: pitcheos promedio por juego
ppj = sp.groupby(["pitcher_anon_id", "game_anon_id"]).size().groupby("pitcher_anon_id").mean().rename("pitcheos_por_juego")
pit = pit.merge(ppj, on="pitcher_anon_id", how="left")
pit["rol"] = np.where(pit["pitcheos_por_juego"] >= 50, "abridor", "relevista")


def z_rel(t, col, minimo):
    q = t[t["n"] >= minimo]
    mu, sd = np.average(q[col], weights=q["n"]), q[col].std()
    return 100 - 10 * (t[col] - mu) / sd


for t, mn in [(pit, 300), (ars, 75)]:
    for nom in ["stuff", "pitching"]:
        for suf in ["mar", "hh"]:
            t[f"{nom}_plus_{suf}_rel"] = z_rel(t, f"xrv_{nom}_{suf}", mn)
    t["cambio_ranking_stuff_hh"] = t["stuff_plus_hh_rel"] - t["stuff_plus_mar_rel"]
    t["cambio_ranking_pitching_hh"] = t["pitching_plus_hh_rel"] - t["pitching_plus_mar_rel"]
pit.round(3).to_csv(os.path.join(R, "scores_pitcher.csv"), index=False)
ars.round(3).to_csv(os.path.join(R, "scores_arsenal.csv"), index=False)

# Diablos
ids = sp[sp["equipo_pitcher"] == "Diablos"].groupby("pitcher_anon_id").size()
ids = ids[ids >= 150].index
casa = sp[sp["pitcher_anon_id"].isin(ids)].assign(sede=lambda x: np.where(x["harp_helu"] == 1, "casa", "visita"))
obs = casa.groupby(["pitcher_anon_id", "sede"]).agg(n=("rv_obs", "size"), rv100=("rv_obs", lambda s: 100 * s.mean())).unstack()
obs.columns = [f"{a}_{b}" for a, b in obs.columns]
dp = pit[pit["pitcher_anon_id"].isin(ids)].merge(obs.reset_index(), on="pitcher_anon_id", how="left")
cols = ["pitcher_anon_id", "rol", "mano", "n", "pitcheos_por_juego", "velo", "ivb", "hb", "gb_bip", "whiff_swing",
        "stuff_plus", "location_plus", "pitching_plus", "stuff_plus_hh_rel", "pitching_plus_hh_rel",
        "cambio_ranking_stuff_hh", "cambio_ranking_pitching_hh", "n_casa", "rv100_casa", "n_visita", "rv100_visita"]
dp = dp[cols].sort_values("pitching_plus_hh_rel", ascending=False)
dp.round(2).to_csv(os.path.join(R, "diablos_pitchers.csv"), index=False)
print(dp.round(1).to_string())

# Arsenal Diablos: Stuff+ HH relativo de cada pitch vs promedio del pitcher (ponderado por uso)
da = ars[ars["pitcher_anon_id"].isin(ids) & (ars["n"] >= 40)].copy()
da["stuff_hh_vs_promedio_pitcher"] = da["stuff_plus_hh_rel"] - da.groupby("pitcher_anon_id")["stuff_plus_hh_rel"].transform(
    lambda s: np.average(s, weights=da.loc[s.index, "n"]))
mezcla = casa.groupby(["pitcher_anon_id", "AutoPitchType", "sede"]).size().unstack(fill_value=0)
mezcla = (100 * mezcla / mezcla.groupby("pitcher_anon_id").transform("sum")).rename(columns={"casa": "uso_casa_%", "visita": "uso_visita_%"}).reset_index()
da = da.merge(mezcla, on=["pitcher_anon_id", "AutoPitchType"], how="left")
da["recomendacion_casa"] = np.select([da["stuff_hh_vs_promedio_pitcher"] >= 5, da["stuff_hh_vs_promedio_pitcher"] <= -5],
                                     ["usar más", "usar menos"], "mantener")
da = da[["pitcher_anon_id", "AutoPitchType", "n", "uso_%", "uso_casa_%", "uso_visita_%", "velo", "ivb", "hb", "stuff_plus",
         "stuff_plus_mar_rel", "stuff_plus_hh_rel", "cambio_ranking_stuff_hh", "stuff_hh_vs_promedio_pitcher", "recomendacion_casa", "rv100"]]
da.round(2).to_csv(os.path.join(R, "diablos_arsenal.csv"), index=False)

# Perfil: dentro de cada tipo, qué rasgos se asocian a perder menos Stuff+ en Harp Helú
perfil = []
for tipo, x in sp[sp["AutoPitchType"].isin(["Four-Seam", "Sinker", "Cutter", "Slider", "Curveball", "Changeup", "Splitter"])].groupby("AutoPitchType"):
    x = x.sample(min(len(x), 60000), random_state=0)
    hbm = np.where(x["PitcherThrows"] == "Left", -x["HorzBreak"], x["HorzBreak"])
    for rasgo, v in [("velocidad", x["RelSpeed"]), ("spin", x["SpinRate"]), ("IVB", x["InducedVertBreak"]),
                     ("|HB|", np.abs(hbm)), ("movimiento total", np.hypot(x["InducedVertBreak"], hbm))]:
        perfil.append({"tipo": tipo, "rasgo": rasgo, "r_con_delta_stuff_hh": round(np.corrcoef(v, x["delta_stuff_hh"])[0, 1], 3),
                       "r_con_stuff_hh": round(np.corrcoef(v, x["stuff_plus_hh"])[0, 1], 3)})
perfil = pd.DataFrame(perfil); perfil.to_csv(os.path.join(R, "perfil_rasgos_vs_delta_altitud.csv"), index=False)
print(perfil.pivot(index="rasgo", columns="tipo", values="r_con_delta_stuff_hh").to_string())
print(perfil.pivot(index="rasgo", columns="tipo", values="r_con_stuff_hh").to_string())

# Liga: mejores pitchers para Harp Helú (ranking relativo, >=500 pitcheos), útil para fichajes/perfil ideal
top = pit[pit["n"] >= 500].sort_values("pitching_plus_hh_rel", ascending=False)
top[["pitcher_anon_id", "equipo", "rol", "mano", "n", "velo", "ivb", "hb", "gb_bip", "stuff_plus", "pitching_plus", "stuff_plus_hh_rel",
     "pitching_plus_hh_rel", "cambio_ranking_pitching_hh"]].head(30).round(2).to_csv(os.path.join(R, "top30_liga_para_harp_helu.csv"), index=False)
