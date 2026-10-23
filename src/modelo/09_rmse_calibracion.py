"""Paso 9: RMSE y calibración fuera de muestra (temporada 2024-25 -> 2026 y parque resto -> Harp Helú).
Calibración = deciles de xRV predicho contra RV observado. Se compara con el baseline del reto (xRV medio por count)."""
import os
import numpy as np, pandas as pd, lightgbm as lgb
from comun import *
from stuffplus import ModeloStuff

d = pd.read_parquet(os.path.join(TRABAJO, "pitches.parquet"))
bip = (d["clase"] == "bip").to_numpy()
mc = lgb.Booster(model_file=os.path.join(MODELOS, "contacto_xrv.txt"))
ok = bip & d["ExitSpeed"].notna().to_numpy() & d["Angle"].notna().to_numpy()
d["xrv_contacto"] = np.nan
d.loc[ok, "xrv_contacto"] = mc.predict(d.loc[ok, ["ExitSpeed", "Angle", "altitude_m"]])
falt = bip & d["xrv_contacto"].isna().to_numpy()
imp = d[bip].groupby(["hit_type", "altitude_category"])["valor_evento"].mean()
d.loc[falt, "xrv_contacto"] = pd.MultiIndex.from_frame(d.loc[falt, ["hit_type", "altitude_category"]]).map(imp)
d.loc[falt & d["xrv_contacto"].isna().to_numpy(), "xrv_contacto"] = d.loc[bip, "valor_evento"].mean()

met = pd.read_csv(os.path.join(RESULTADOS, "metricas_holdout_pitcher.csv"))
arb = {(r.modelo, r.cabeza): int(r.arboles) for r in met.itertuples()}
base = dict(learning_rate=0.08, num_leaves=63, min_data_in_leaf=300, feature_fraction=0.85,
            bagging_fraction=0.8, bagging_freq=1, lambda_l2=5.0, verbose=-1, num_threads=8)
y = d["clase"].map({k: i for i, k in enumerate(CLASES)})
F = {"stuff": FEATS_STUFF, "pitch": FEATS_PITCH}
filas, cal = [], []
for nombre, tr in [("temporada 2024-25 -> 2026", (d["year"] < 2026).to_numpy()),
                   ("parque resto -> Harp Helú", (d["harp_helu"] == 0).to_numpy())]:
    te = ~tr
    bc = d[tr].groupby("count_k")["rv_obs"].mean()
    t = d[te].copy(); t["base"] = t["count_k"].map(bc).fillna(d.loc[tr, "rv_obs"].mean())
    for fs in ["stuff", "pitch"]:
        a = lgb.train(base | dict(objective="multiclass", num_class=len(CLASES)), lgb.Dataset(d.loc[tr, F[fs]], y[tr]), arb[(fs, "clase")])
        b = lgb.train(base | dict(objective="regression"), lgb.Dataset(d.loc[tr & bip, F[fs]], d.loc[tr & bip, "xrv_contacto"]), arb[(fs, "bip_xrv")])
        M = ModeloStuff(); M.m = {(fs, "clase"): a, (fs, "bip_xrv"): b}
        x = M.predecir(t, fs)["xrv"].to_numpy()
        # Stuff no ve el count: se compara su xRV + el valor medio del count (misma referencia que el baseline)
        pred = x + t["base"].to_numpy() if fs == "stuff" else x
        r = t["rv_obs"].to_numpy()
        pp = pd.DataFrame({"p": t["pitcher_anon_id"], "r": r, "x": pred, "b": t["base"]}).groupby("p").agg(n=("r", "size"), r=("r", "mean"), x=("x", "mean"), b=("b", "mean"))
        pp = pp[pp.n >= 200]
        filas.append({"validacion": nombre, "modelo": fs, "n_pitcheos": len(r),
                      "rmse_pitcheo": np.sqrt(np.mean((r - pred) ** 2)), "rmse_pitcheo_baseline": np.sqrt(np.mean((r - t["base"]) ** 2)),
                      "pitchers_200+": len(pp),
                      "rmse_pitcher_rv100": 100 * np.sqrt(np.mean((pp.r - pp.x) ** 2)), "rmse_pitcher_rv100_baseline": 100 * np.sqrt(np.mean((pp.r - pp.b) ** 2)),
                      "pendiente_calibracion": np.polyfit(pred, r, 1)[0]})
        dec = pd.qcut(pred, 10, labels=False, duplicates="drop")
        c = pd.DataFrame({"decil": dec + 1, "pred": pred, "obs": r}).groupby("decil").agg(xrv_predicho=("pred", "mean"), rv_observado=("obs", "mean"), n=("obs", "size"))
        c.insert(0, "modelo", fs); c.insert(0, "validacion", nombre); cal.append(c.reset_index())
        print(filas[-1], flush=True)
pd.DataFrame(filas).round(4).to_csv(os.path.join(RESULTADOS, "rmse_holdout.csv"), index=False)
pd.concat(cal).round(4).to_csv(os.path.join(RESULTADOS, "calibracion_deciles.csv"), index=False)
