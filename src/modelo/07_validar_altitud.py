"""Paso 7: validación externa del efecto altitud. Mismos pitchers (>=250 pitcheos en parques >=1,800 m y en <700 m):
¿el modelo reproduce cuánto peor les va en altura, en promedio y pitcher por pitcher?"""
import os
import numpy as np
import pandas as pd
from comun import *

sp = pd.read_parquet(os.path.join(RESULTADOS, "scores_pitch.parquet"))
sp["env"] = np.where(sp["altitude_m"] >= 1800, "alta", np.where(sp["altitude_m"] < 700, "baja", "media"))
g = sp[sp["env"] != "media"].groupby(["pitcher_anon_id", "env"]).agg(
    n=("rv_obs", "size"), rv=("rv_obs", "mean"), xs=("xrv_stuff", "mean"), xp=("xrv_pitching", "mean"),
    d=("delta_stuff_hh", "mean")).unstack()
g = g[(g[("n", "alta")] >= 250) & (g[("n", "baja")] >= 250)]
obs = 100 * (g[("rv", "alta")] - g[("rv", "baja")])
pred_d = -g[("d", "baja")]  # pérdida predicha al llevar su repertorio de nivel del mar a Harp Helú
out = pd.DataFrame([{
    "pitchers": len(g),
    "rv100_observado_alta_menos_baja": round(obs.mean(), 2),
    "xrv100_stuff_modelo_alta_menos_baja": round(100 * (g[("xs", "alta")] - g[("xs", "baja")]).mean(), 2),
    "xrv100_pitching_modelo_alta_menos_baja": round(100 * (g[("xp", "alta")] - g[("xp", "baja")]).mean(), 2),
    "r_perdida_predicha_vs_observada_por_pitcher": round(np.corrcoef(pred_d - pred_d.mean(), obs - obs.mean())[0, 1], 3),
}])
out.to_csv(os.path.join(RESULTADOS, "validacion_efecto_altitud.csv"), index=False)
print(out.T)
