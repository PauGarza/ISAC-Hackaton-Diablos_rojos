"""Paso 4: validación por temporada (2024-25 -> 2026), por parque (sin Harp Helú -> Harp Helú) y por pitcher
(ver metricas_holdout_pitcher.csv del paso 3). Compara contra el baseline del reto (xRV medio por count),
estabilidad año a año, poder predictivo, y prueba H4 (spin solo vs. forma completa)."""
import os, json
import numpy as np
import pandas as pd
import lightgbm as lgb
from comun import *
from stuffplus import ModeloStuff

d = pd.read_parquet(os.path.join(TRABAJO, "pitches.parquet")).merge(
    pd.read_parquet(os.path.join(TRABAJO, "contacto.parquet")), on="fila")
met = pd.read_csv(os.path.join(RESULTADOS, "metricas_holdout_pitcher.csv"))
arb = {(r.modelo, r.cabeza): int(r.arboles) for r in met.itertuples()}
base = dict(learning_rate=0.08, num_leaves=63, min_data_in_leaf=300, feature_fraction=0.85,
            bagging_fraction=0.8, bagging_freq=1, lambda_l2=5.0, verbose=-1, num_threads=4)
y_clase = d["clase"].map({k: i for i, k in enumerate(CLASES)})
bip = (d["clase"] == "bip").to_numpy()
FEATS_H4 = ["RelSpeed", "SpinRate", "es_zurdo", "mismo_lado", "altitude_m"]


def entrenar(fs, tr, feats=None):
    feats = feats or {"stuff": FEATS_STUFF, "loc": FEATS_LOC, "pitch": FEATS_PITCH}[fs]
    a = lgb.train(base | dict(objective="multiclass", num_class=len(CLASES)),
                  lgb.Dataset(d.loc[tr, feats], y_clase[tr]), arb[(fs, "clase")])
    b = lgb.train(base | dict(objective="regression"), lgb.Dataset(d.loc[tr & bip, feats], d.loc[tr & bip, "xrv_contacto"]), arb[(fs, "bip_xrv")])
    return a, b


def evaluar(nombre, fs, tr, te, feats=None, etiqueta=None):
    a, b = entrenar(fs, tr, feats)
    M = ModeloStuff(); M.m = {(fs, "clase"): a, (fs, "bip_xrv"): b}
    if feats:  # ablación: predecir con features reducidas
        global FEATS_STUFF_ORIG
        from stuffplus import FEATS as F
        F[fs + "_h4"] = feats; M.m = {(fs + "_h4", "clase"): a, (fs + "_h4", "bip_xrv"): b}
        M.esc[fs + "_h4"] = M.esc[fs]; fs_eval = fs + "_h4"
        # predecir() solo distingue 'stuff' para la fórmula sin count
        x = d[te].copy()
        P = a.predict(x[feats]); bx = b.predict(x[feats])
        rvbar = M.esc["rv_medio_clase"]
        xrv = sum(P[:, i] * rvbar[c] for i, c in enumerate(CLASES) if c != "bip") + P[:, CLASES.index("bip")] * (bx - M.esc["v_count_medio_bip"])
        pr = pd.DataFrame({"xrv": xrv}, index=x.index); P_te = P
    else:
        pr = M.predecir(d[te], fs); P_te = pr[[f"p_{c}" for c in CLASES]].to_numpy()
    yt = y_clase[te].to_numpy()
    ll = -np.mean(np.log(np.clip(P_te[np.arange(len(yt)), yt], 1e-12, 1)))
    fr = np.bincount(y_clase[tr], minlength=len(CLASES)) / tr.sum()
    ll0 = -np.mean(np.log(fr[yt]))
    t = d[te].assign(xrv=pr["xrv"].to_numpy())
    # baseline del reto: xRV medio por count (aprendido en train)
    bc = d[tr].groupby("count_k")["rv_obs"].mean()
    t["base_count"] = t["count_k"].map(bc)
    mse = np.mean((t["rv_obs"] - t["xrv"]) ** 2); mse0 = np.mean((t["rv_obs"] - t["base_count"]) ** 2)
    pp = t.groupby("pitcher_anon_id").agg(n=("rv_obs", "size"), rv=("rv_obs", "mean"), xrv=("xrv", "mean"), bc=("base_count", "mean"))
    pp = pp[pp["n"] >= 200]
    out = {"validacion": nombre, "modelo": etiqueta or fs, "n_test": int(te.sum()), "logloss": round(ll, 4),
           "logloss_constante": round(ll0, 4), "mejora_logloss_%": round(100 * (1 - ll / ll0), 2),
           "mse_rv_x1000": round(1000 * mse, 3), "mse_baseline_count_x1000": round(1000 * mse0, 3),
           "mejora_mse_vs_baseline_%": round(100 * (1 - mse / mse0), 2),
           "pitchers_200+": len(pp), "r_pitcher_xrv_vs_rv": round(pp[["xrv", "rv"]].corr().iat[0, 1], 3),
           "r_pitcher_baseline_vs_rv": round(pp[["bc", "rv"]].corr().iat[0, 1], 3)}
    print(out, flush=True)
    return out


filas = []
tr = (d["year"] < 2026).to_numpy(); te = ~tr
for fs in ["stuff", "loc", "pitch"]:
    filas.append(evaluar("temporada: 2024-25 -> 2026", fs, tr, te))
tr = (d["harp_helu"] == 0).to_numpy(); te = ~tr
for fs in ["stuff", "pitch"]:
    filas.append(evaluar("parque: resto -> Harp Helú", fs, tr, te))
tr = (d["holdout_pitcher"] == 0).to_numpy(); te = ~tr
filas.append(evaluar("pitcher: 85% -> 15% (H4)", "stuff", tr, te))
filas.append(evaluar("pitcher: 85% -> 15% (H4)", "stuff", tr, te, feats=FEATS_H4, etiqueta="stuff_solo_velo_spin"))
filas.append(evaluar("pitcher: 85% -> 15% (H4)", "stuff", tr, te, feats=FEATS_H4 + ["ivb", "hb_m", "spin_axis_m"], etiqueta="stuff_velo_spin_mov"))
pd.DataFrame(filas).to_csv(os.path.join(RESULTADOS, "validacion.csv"), index=False)
