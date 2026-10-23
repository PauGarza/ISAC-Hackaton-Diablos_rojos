"""Paso 2 (H1): cuánto se reduce el movimiento inducido por spin con la altitud.
Comparación dentro del mismo pitcher x tipo x temporada: media en cada estadio vs. su media
en parques bajos (<700 m). Modelo físico: mov(alt) = mov(0) * exp(-k * alt_km), k por tipo y
componente (IVB, HB). Por densidad del aire (atmósfera estándar) se esperaría k ~ 0.10 /km."""
import os, json
import numpy as np
import pandas as pd
from comun import *

d = pd.read_parquet(os.path.join(TRABAJO, "pitches.parquet"),
                    columns=["pitcher_anon_id", "year", "AutoPitchType", "estadio", "altitude_m", "ivb", "hb_m", "RelSpeed", "SpinRate", "SpeedDrop"])
g = d.groupby(["pitcher_anon_id", "year", "AutoPitchType", "estadio"]).agg(
    alt=("altitude_m", "first"), n=("ivb", "size"), ivb=("ivb", "mean"), hb=("hb_m", "mean"),
    velo=("RelSpeed", "mean"), spin=("SpinRate", "mean"), drop=("SpeedDrop", "mean")).reset_index()
g = g[g["n"] >= 8]
bajo = g[g["alt"] < 700].copy()
bajo["w"] = bajo["n"]
ref = bajo.groupby(["pitcher_anon_id", "year", "AutoPitchType"]).apply(
    lambda x: pd.Series({c + "_0": np.average(x[c], weights=x["w"]) for c in ["ivb", "hb", "velo", "spin", "drop"]} | {"n0": x["n"].sum()}),
    include_groups=False).reset_index()
m = g[g["alt"] >= 700].merge(ref, on=["pitcher_anon_id", "year", "AutoPitchType"])
m["alt_km"] = m["alt"] / 1000
res, filas = {}, []
for tipo, x in m.groupby("AutoPitchType"):
    res[tipo] = {}
    for comp, umbral in [("ivb", 4.0), ("hb", 4.0)]:
        y = x[x[comp + "_0"].abs() >= umbral]
        if len(y) < 30:
            continue
        r = (y[comp] / y[comp + "_0"]).clip(0.2, 2.0)
        w = np.minimum(y["n"], y["n0"])
        lr = np.log(r)
        k = -np.sum(w * lr * y["alt_km"]) / np.sum(w * y["alt_km"] ** 2)
        # error estándar por bootstrap de pitchers
        pits = y["pitcher_anon_id"].unique(); rng = np.random.default_rng(0); ks = []
        idx = {p: np.where(y["pitcher_anon_id"].values == p)[0] for p in pits}
        for _ in range(200):
            ii = np.concatenate([idx[p] for p in rng.choice(pits, len(pits))])
            ks.append(-np.sum(w.values[ii] * lr.values[ii] * y["alt_km"].values[ii]) / np.sum(w.values[ii] * y["alt_km"].values[ii] ** 2))
        res[tipo][comp] = float(k)
        filas.append({"tipo": tipo, "componente": comp, "k_por_km": round(k, 4), "ee": round(float(np.std(ks)), 4),
                      "ratio_harp_helu": round(float(np.exp(-k * 2.24)), 3), "n_comparaciones": len(y),
                      "n_pitchers": len(pits)})
# Cambio absoluto en Harp Helú vs nivel del mar, mismo pitcher (pulgadas), y velocidad/spin sin cambio
hh = m[m["alt"] >= 2200]
abs_tab = hh.assign(d_ivb=hh["ivb"] - hh["ivb_0"], d_hb=hh["hb"] - hh["hb_0"], d_velo=hh["velo"] - hh["velo_0"],
                    d_spin=hh["spin"] - hh["spin_0"], d_drop=hh["drop"] - hh["drop_0"]).groupby("AutoPitchType").apply(
    lambda x: pd.Series({c: np.average(x[c], weights=np.minimum(x["n"], x["n0"])) for c in ["d_ivb", "d_hb", "d_velo", "d_spin", "d_drop"]} | {"n_pitchers": x["pitcher_anon_id"].nunique()}),
    include_groups=False).round(2)
print(pd.DataFrame(filas).to_string()); print(abs_tab.to_string())
# Valor por defecto (todos los tipos) para tipos raros
for comp in ["ivb", "hb"]:
    vals = [f for f in filas if f["componente"] == comp]
    res.setdefault("_global", {})[comp] = float(np.average([f["k_por_km"] for f in vals], weights=[f["n_comparaciones"] for f in vals]))
# Splitter tiene muy pocas comparaciones: usar los k del changeup (misma familia). Cutter sin HB fiable: global.
res["Splitter"] = dict(res["Changeup"]); res["Sweeper"] = dict(res["Slider"])
res.setdefault("Cutter", {}).setdefault("hb", res["_global"]["hb"])
json.dump(res, open(os.path.join(MODELOS, "k_altitud.json"), "w"), indent=1)
pd.DataFrame(filas).to_csv(os.path.join(RESULTADOS, "h1_k_altitud_por_tipo.csv"), index=False)
abs_tab.to_csv(os.path.join(RESULTADOS, "h1_cambio_harp_helu_vs_nivel_mar_mismo_pitcher.csv"))
