"""Castigo de altitud por pitcher x tipo de pitcheo con un modelo jerárquico normal-normal (Bayes empírico).

Dato por pitcher-tipo j: d_j = RV/100 observado en parques >=1,800 m menos RV/100 en parques <700 m
(positivo = peor en altura), con error estándar se_j.
Modelo:  d_j ~ N(theta_j, se_j^2);  theta_j ~ N(a_t + b * pred_j, tau_t^2)
donde pred_j = castigo que predice el LightGBM (-Δ Stuff+ Harp Helú vs mar, en carreras/100) y t = tipo.
Hiperparámetros (a_t, b, tau_t) por máxima verosimilitud marginal. Posterior: encogimiento hacia la
predicción del modelo según la muestra. Pitchers sin datos en ambos entornos reciben la predictiva previa.
"""
import os
import numpy as np, pandas as pd
from scipy.optimize import minimize

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
R = os.path.join(RAIZ, "outputs", "resultados") + "/"
OUT = os.path.join(RAIZ, "results", "bayes_mcmc") + "/"
p = pd.read_parquet(R + "scores_pitch.parquet",
                    columns=["pitcher_anon_id", "AutoPitchType", "altitude_m", "rv_obs", "delta_stuff_hh", "equipo_pitcher", "year"])
p = p.dropna(subset=["pitcher_anon_id"])
tipos = ["Four-Seam", "Sinker", "Cutter", "Slider", "Curveball", "Changeup", "Splitter"]
p = p[p.AutoPitchType.isin(tipos)]
p["amb"] = np.select([p.altitude_m >= 1800, p.altitude_m < 700], ["alto", "bajo"], "medio")
p["pred"] = -0.126 * p.delta_stuff_hh  # 10 puntos Stuff+ = 1.26 carreras/100

k = ["pitcher_anon_id", "AutoPitchType"]
pred = p.groupby(k).agg(pred=("pred", "mean"), n_total=("pred", "size"))
eq = p.sort_values("year").groupby("pitcher_anon_id").equipo_pitcher.last()
sd_pitch = p.rv_obs.std()
g = p[p.amb != "medio"].groupby(k + ["amb"]).rv_obs.agg(["mean", "size"]).unstack()
g = g.dropna()
g = g[(g[("size", "alto")] >= 30) & (g[("size", "bajo")] >= 30)]
obs = pd.DataFrame({
    "d": 100 * (g[("mean", "alto")] - g[("mean", "bajo")]),
    "se": 100 * sd_pitch * np.sqrt(1 / g[("size", "alto")] + 1 / g[("size", "bajo")]),
    "n_alto": g[("size", "alto")], "n_bajo": g[("size", "bajo")]})
obs = obs.join(pred)
ti = obs.index.get_level_values(1)
T = {t: i for i, t in enumerate(tipos)}
ix = np.array([T[t] for t in ti])

def nll(th):
    a = th[:7]; b = th[7]; tau = np.exp(th[8:15])
    m = a[ix] + b * obs.pred.values
    v = tau[ix] ** 2 + obs.se.values ** 2
    return 0.5 * np.sum(np.log(v) + (obs.d.values - m) ** 2 / v)

r = minimize(nll, np.r_[np.zeros(7), 1.0, np.zeros(7)], method="L-BFGS-B")
a, b, tau = r.x[:7], r.x[7], np.exp(r.x[8:15])
hyper = pd.DataFrame({"tipo": tipos, "a_t": a, "tau_t": tau, "b": b, "n_pitcher_tipo": [np.sum(ix == i) for i in range(7)]})
hyper.round(3).to_csv(OUT + "hiperparametros_bayes_empirico.csv", index=False)

# Posterior para todos los pitcher-tipo (con o sin datos en ambos entornos)
todo = pred.join(obs[["d", "se", "n_alto", "n_bajo"]])
ti_all = np.array([T[t] for t in todo.index.get_level_values(1)])
m0 = a[ti_all] + b * todo.pred.values
v0 = tau[ti_all] ** 2
se2 = todo.se.values ** 2
hay = ~np.isnan(se2)
vpost = np.where(hay, 1 / (1 / v0 + 1 / np.where(hay, se2, 1)), v0)
mpost = np.where(hay, vpost * (m0 / v0 + np.nan_to_num(todo.d.values) / np.where(hay, se2, 1)), m0)
todo["castigo_prior"] = m0
todo["castigo_post"] = mpost
todo["p10"] = mpost - 1.2816 * np.sqrt(vpost)
todo["p90"] = mpost + 1.2816 * np.sqrt(vpost)
todo["peso_datos"] = np.where(hay, v0 / (v0 + np.where(hay, se2, 1)), 0.0)
todo["equipo"] = todo.index.get_level_values(0).map(eq)
todo = todo.rename(columns={"pred": "castigo_lgbm", "d": "castigo_observado", "se": "se_observado"})
todo.reset_index().round(3).to_csv(OUT + "castigo_altitud_bayes_empirico.csv", index=False)

# Validación: predecir mitad de los pitcheos de altura con la otra mitad (split por paridad de fila)
print("b =", round(b, 3)); print(hyper.round(3).to_string(index=False))
print("pitcher-tipo con datos en ambos entornos:", len(obs), " de", len(todo))
print("peso medio de los datos:", round(todo.peso_datos[hay].mean(), 3))
print("corr castigo observado vs lgbm:", round(np.corrcoef(obs.d, obs.pred)[0, 1], 3))
