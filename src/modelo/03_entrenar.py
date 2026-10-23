"""Paso 3: modelo de contacto (xRV por EV/LA/altitud) y modelos LightGBM de Stuff+, Location+ y Pitching+.
Cada familia tiene 5 cabezas: desenlace multiclase (ball/called/whiff/foul/bip/hbp), xRV del contacto,
P(rodado), P(contacto duro >=95 mph), P(out | bip). Holdout por pitcher (15 %) para escoger número
de árboles y medir; luego se reentrena con todos los datos."""
import os, json, time
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import GroupShuffleSplit
from comun import *

os.makedirs(MODELOS, exist_ok=True)
d = pd.read_parquet(os.path.join(TRABAJO, "pitches.parquet"))
bip = d["clase"] == "bip"

# ---------- 1. Modelo de contacto: valor esperado del evento dado EV, LA y altitud ----------
cfe = ["ExitSpeed", "Angle", "altitude_m"]
c = d[bip & d["ExitSpeed"].notna() & d["Angle"].notna()]
pc = dict(objective="regression", learning_rate=0.05, num_leaves=31, min_data_in_leaf=200, verbose=-1, num_threads=4)
mc = lgb.train(pc, lgb.Dataset(c[cfe], c["valor_evento"]), 400)
mc.save_model(os.path.join(MODELOS, "contacto_xrv.txt"))
d["xrv_contacto"] = np.nan
d.loc[c.index, "xrv_contacto"] = mc.predict(c[cfe])
falt = bip & d["xrv_contacto"].isna()
imp = d[bip].groupby(["hit_type", "altitude_category"])["valor_evento"].mean()
d.loc[falt, "xrv_contacto"] = pd.MultiIndex.from_frame(d.loc[falt, ["hit_type", "altitude_category"]]).map(imp)
d.loc[falt & d["xrv_contacto"].isna(), "xrv_contacto"] = d.loc[bip, "valor_evento"].mean()
print("contacto listo; corr xrv_contacto vs valor_evento:", round(d.loc[c.index, ["xrv_contacto", "valor_evento"]].corr().iat[0, 1], 3))

# ---------- 2. Constantes de escala ----------
esc = {"rv_medio_clase": d.groupby("clase")["rv_obs"].mean().to_dict(),
       "v_count_medio_bip": float(d.loc[bip, "v_count"].mean())}
fbl = d[(d["AutoPitchType"] == "Four-Seam") & (d["altitude_m"] < 700)]
esc["fb_liga"] = {"fb_velo": float(fbl["RelSpeed"].mean()), "fb_ivb": float(fbl["ivb"].mean()),
                  "fb_hb": float(fbl["hb_m"].mean()), "fb_axis": float(fbl["spin_axis_m"].mean())}

gss = GroupShuffleSplit(n_splits=1, test_size=0.15, random_state=7)
itr, ite = next(gss.split(d, groups=d["pitcher_anon_id"].fillna("NA").astype(str).to_numpy()))
d["holdout_pitcher"] = 0
d.loc[d.index[ite], "holdout_pitcher"] = 1

base = dict(learning_rate=0.08, num_leaves=63, min_data_in_leaf=300, feature_fraction=0.85,
            bagging_fraction=0.8, bagging_freq=1, lambda_l2=5.0, verbose=-1, num_threads=4)
cabezas = {
    "clase": (None, dict(objective="multiclass", num_class=len(CLASES), metric="multi_logloss")),
    "bip_xrv": ("bip", dict(objective="regression", metric="l2")),
    "gb": ("gb", dict(objective="binary", metric="binary_logloss")),
    "hard": ("hard", dict(objective="binary", metric="binary_logloss")),
    "out_bip": ("out_bip", dict(objective="binary", metric="binary_logloss")),
}
y_clase = d["clase"].map({k: i for i, k in enumerate(CLASES)})
metricas = []
for fs, feats in [("stuff", FEATS_STUFF), ("loc", FEATS_LOC), ("pitch", FEATS_PITCH)]:
    for h, (filtro, obj) in cabezas.items():
        t0 = time.time()
        if h == "clase":
            m, y = np.ones(len(d), bool), y_clase
        elif h == "bip_xrv":
            m, y = bip.to_numpy(), d["xrv_contacto"]
        else:
            m, y = d[filtro].notna().to_numpy(), d[filtro]
        tr = m & (d["holdout_pitcher"] == 0).to_numpy(); te = m & (d["holdout_pitcher"] == 1).to_numpy()
        p = base | obj
        dtr = lgb.Dataset(d.loc[tr, feats], y[tr]); dte = lgb.Dataset(d.loc[te, feats], y[te], reference=dtr)
        mod = lgb.train(p, dtr, 1500, valid_sets=[dte], callbacks=[lgb.early_stopping(40, verbose=False)])
        best = mod.best_iteration
        score = mod.best_score["valid_0"][obj["metric"]]
        # referencia: predicción constante (o por count para loc/pitch no aplica aquí)
        if h == "clase":
            fr = np.bincount(y[tr], minlength=len(CLASES)) / tr.sum()
            ref = -np.mean(np.log(fr[y[te]]))
        elif obj["objective"] == "binary":
            pm = y[tr].mean(); yt = y[te]
            ref = -np.mean(yt * np.log(pm) + (1 - yt) * np.log(1 - pm))
        else:
            ref = np.mean((y[te] - y[tr].mean()) ** 2)
        final = lgb.train(p, lgb.Dataset(d.loc[m, feats], y[m]), max(best, 50))
        final.save_model(os.path.join(MODELOS, f"{fs}_{h}.txt"))
        metricas.append({"modelo": fs, "cabeza": h, "metrica": obj["metric"], "holdout_pitcher": round(score, 5),
                         "referencia_constante": round(float(ref), 5), "mejora_%": round(100 * (1 - score / ref), 2),
                         "arboles": best, "seg": round(time.time() - t0)})
        print(metricas[-1], flush=True)
pd.DataFrame(metricas).to_csv(os.path.join(RESULTADOS, "metricas_holdout_pitcher.csv"), index=False)

# ---------- 3. Escala: media y sd del xRV por pitcheo en la liga (entorno nativo) ----------
json.dump(esc | {"stuff": {"media": 0, "sd": 1}, "loc": {"media": 0, "sd": 1}, "pitch": {"media": 0, "sd": 1}},
          open(os.path.join(MODELOS, "escala.json"), "w"))
from stuffplus import ModeloStuff
M = ModeloStuff()
for fs in ["stuff", "loc", "pitch"]:
    x = M.predecir(d, fs)["xrv"]
    esc[fs] = {"media": float(x.mean()), "sd": float(x.std())}
json.dump(esc, open(os.path.join(MODELOS, "escala.json"), "w"), indent=1)
d[["fila", "xrv_contacto", "holdout_pitcher"]].to_parquet(os.path.join(TRABAJO, "contacto.parquet"), index=False)
print("escala:", {k: esc[k] for k in ["stuff", "loc", "pitch"]})
