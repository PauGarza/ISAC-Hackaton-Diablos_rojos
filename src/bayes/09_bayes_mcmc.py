"""Castigo de altitud por pitcher x tipo de pitcheo, modelo jerárquico completamente bayesiano (MCMC, PyMC/NUTS).

Mismo modelo que 08_bayes_jerarquico.py, pero los hiperparámetros tienen priori y se integran por MCMC,
así que su incertidumbre entra a los intervalos.

  Verosimilitud:  d_j ~ N(theta_j, se_j^2)
  Priori:         theta_j ~ N(a_t + b * pred_j, tau_t^2)
  Hiperprioris:   a_t ~ N(0, 2),  b ~ N(1, 0.5),  tau_t ~ HalfNormal(1.5)     (carreras/100)

d_j = RV/100 en parques >=1,800 m menos RV/100 en parques <700 m; pred_j = castigo que predice el LightGBM.
Parametrización no centrada: theta_j = mu_j + tau_t * z_j, z_j ~ N(0, 1).
Muestreo: 2 cadenas x 5,000 muestras (10,000 en total), 2,000 de calentamiento por cadena.
"""
import os
import numpy as np, pandas as pd, pymc as pm, arviz as az

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
R = os.path.join(RAIZ, "outputs", "resultados") + "/"
OUT = os.path.join(RAIZ, "results", "bayes_mcmc") + "/"
tipos = ["Four-Seam", "Sinker", "Cutter", "Slider", "Curveball", "Changeup", "Splitter"]
T = {t: i for i, t in enumerate(tipos)}

p = pd.read_parquet(R + "scores_pitch.parquet",
                    columns=["pitcher_anon_id", "AutoPitchType", "altitude_m", "rv_obs", "delta_stuff_hh", "equipo_pitcher", "year"])
p = p.dropna(subset=["pitcher_anon_id"])
p = p[p.AutoPitchType.isin(tipos)]
p["amb"] = np.select([p.altitude_m >= 1800, p.altitude_m < 700], ["alto", "bajo"], "medio")
p["pred"] = -0.126 * p.delta_stuff_hh  # 10 puntos Stuff+ = 1.26 carreras/100

k = ["pitcher_anon_id", "AutoPitchType"]
pred = p.groupby(k).agg(pred=("pred", "mean"), n_total=("pred", "size"))
eq = p.sort_values("year").groupby("pitcher_anon_id").equipo_pitcher.last()
sd_pitch = p.rv_obs.std()
g = p[p.amb != "medio"].groupby(k + ["amb"]).rv_obs.agg(["mean", "size"]).unstack().dropna()
g = g[(g[("size", "alto")] >= 30) & (g[("size", "bajo")] >= 30)]
obs = pd.DataFrame({
    "d": 100 * (g[("mean", "alto")] - g[("mean", "bajo")]),
    "se": 100 * sd_pitch * np.sqrt(1 / g[("size", "alto")] + 1 / g[("size", "bajo")]),
    "n_alto": g[("size", "alto")], "n_bajo": g[("size", "bajo")]}).join(pred)
ix = np.array([T[t] for t in obs.index.get_level_values(1)])

with pm.Model() as m:
    a = pm.Normal("a", 0, 2, shape=7)
    b = pm.Normal("b", 1, 0.5)
    tau = pm.HalfNormal("tau", 1.5, shape=7)
    z = pm.Normal("z", 0, 1, shape=len(obs))
    theta = pm.Deterministic("theta", a[ix] + b * obs.pred.values + tau[ix] * z)
    pm.Normal("d", theta, obs.se.values, observed=obs.d.values)
    tr = pm.sample(draws=5000, tune=2000, chains=2, cores=2, target_accept=0.95, random_seed=2026, progressbar=False)

mues = {"cadena": np.repeat([0, 1], tr.posterior["b"].values.shape[1]), "b": tr.posterior["b"].values.reshape(-1)}
for v in ["a", "tau"]:
    for i, t in enumerate(tipos):
        mues[f"{v}_{t}"] = tr.posterior[v].values[:, :, i].reshape(-1)
pd.DataFrame(mues).to_csv(OUT + "muestras_hiperparametros.csv.gz", index=False)
resumen = az.summary(tr, var_names=["a", "b", "tau"], ci_prob=0.8)
resumen.index = [i.replace("[", "_").replace("]", "") for i in resumen.index]
nom = {f"a_{i}": f"a_{t}" for i, t in enumerate(tipos)} | {f"tau_{i}": f"tau_{t}" for i, t in enumerate(tipos)}
resumen.rename(index=nom).to_csv(OUT + "hiperparametros_mcmc.csv")
diag = az.summary(tr, var_names=["theta"])
conv = pd.DataFrame([{
    "divergencias": int(tr.sample_stats.diverging.sum()),
    "rhat_max_hiper": resumen.r_hat.max(), "rhat_max_theta": diag.r_hat.max(),
    "ess_bulk_min_hiper": resumen.ess_bulk.min(), "ess_tail_min_hiper": resumen.ess_tail.min(),
    "ess_bulk_min_theta": diag.ess_bulk.min(), "ess_tail_min_theta": diag.ess_tail.min(),
    "max_treedepth_hits": int((tr.sample_stats.tree_depth >= 10).sum())}])
conv.to_csv(OUT + "convergencia.csv", index=False)

# Autocorrelación de las muestras por cadena (lags 1, 5, 10, 20): cerca de 0 = muestras casi independientes.
def acf(x, lag):
    x = x - x.mean()
    return float(np.dot(x[:-lag], x[lag:]) / np.dot(x, x))
filas = []
for v in ["a", "b", "tau"]:
    arr = tr.posterior[v].values  # (cadena, muestra[, tipo])
    arr = arr[..., None] if arr.ndim == 2 else arr
    for j in range(arr.shape[2]):
        nombre = v if v == "b" else f"{v}_{tipos[j]}"
        fila = {"parametro": nombre}
        for lag in [1, 5, 10, 20]:
            fila[f"acf_lag{lag}"] = np.mean([acf(arr[c, :, j], lag) for c in range(arr.shape[0])])
        filas.append(fila)
ac = pd.DataFrame(filas)
ac.round(3).to_csv(OUT + "autocorrelacion.csv", index=False)
print(ac.round(3).to_string(index=False))
print(conv.T.to_string())

# Posterior de cada pitcher-tipo. Con datos: muestras de theta. Sin datos: predictiva a_t + b*pred + tau_t*N(0,1).
post = tr.posterior
A = post.a.values.reshape(-1, 7); B = post.b.values.reshape(-1); TAU = post.tau.values.reshape(-1, 7)
TH = post.theta.values.reshape(-1, len(obs))
rng = np.random.default_rng(2026)
todo = pred.join(obs[["d", "se", "n_alto", "n_bajo"]])
pos = {key: i for i, key in enumerate(obs.index)}
filas = []
for key, r in todo.iterrows():
    t = T[key[1]]
    s = TH[:, pos[key]] if key in pos else A[:, t] + B * r.pred + TAU[:, t] * rng.standard_normal(len(B))
    filas.append({"castigo_post": s.mean(), "p10": np.quantile(s, .1), "p90": np.quantile(s, .9),
                  "p_mayor_3": (s > 3).mean()})
res = todo.reset_index().join(pd.DataFrame(filas))
res["equipo"] = res.pitcher_anon_id.map(eq)
res = res.rename(columns={"pred": "castigo_lgbm", "d": "castigo_observado", "se": "se_observado"})
res.round(3).to_csv(OUT + "castigo_altitud_pitcher_tipo_mcmc.csv", index=False)
print(resumen.rename(index=nom).round(3).to_string())
