# Modelo bayesiano jerárquico con MCMC (2026-10-18)

Código: `09_bayes_mcmc.py` (PyMC 5.x, muestreador NUTS; diagnósticos con ArviZ). Mismo modelo que `08_bayes_jerarquico.py`, pero completamente bayesiano: los hiperparámetros tienen priori y se integran por MCMC.

## Modelo
- Verosimilitud: d_j ~ N(θ_j, se_j²), con d_j = RV/100 en parques ≥1,800 m − RV/100 en parques <700 m.
- Priori: θ_j ~ N(a_t + b·pred_j, τ_t²), con pred_j = castigo que predice el LightGBM por la forma.
- Hiperprioris (débilmente informativas, en carreras/100): a_t ~ N(0, 2), b ~ N(1, 0.5), τ_t ~ HalfNormal(1.5).
- Parametrización no centrada (θ_j = μ_j + τ_t·z_j) para evitar divergencias.
- 2 cadenas × 5,000 muestras = 10,000, más 2,000 de calentamiento por cadena, target_accept = 0.95.

## Convergencia (`convergencia.csv`)
| Criterio | Valor | Umbral usual |
|---|---|---|
| Divergencias | 0 | 0 |
| R-hat máximo (hiperparámetros / θ) | 1.001 / 1.002 | < 1.01 |
| ESS bulk mínimo (hiper / θ) | 1,686 / 3,788 | > 400 |
| ESS tail mínimo (hiper / θ) | 1,923 / 5,278 | > 400 |
| Iteraciones que tocan la profundidad máxima | 0 | 0 |

## Autocorrelación de las muestras (`autocorrelacion.csv`)
Lag 1 entre −0.12 y 0.55; lag 5 ≤ 0.15; lag 10 ≤ 0.06; lag 20 ≤ 0.02. Las muestras son prácticamente independientes a partir de ~10 pasos. El ESS ya descuenta esa correlación: las 10,000 muestras equivalen a por lo menos 1,686 independientes en el peor parámetro (τ del changeup). No hace falta adelgazar (*thinning*); si se quisieran muestras casi independientes, quedarse con 1 de cada 10 deja 1,000.

## Hiperparámetros (`hiperparametros_mcmc.csv`, media e intervalo de 80 %)
| Tipo | a_t | τ_t |
|---|---|---|
| Recta | −0.23 (−0.92 a 0.46) | 0.47 (0.08 a 0.91) |
| Sinker | 0.37 (−0.22 a 0.97) | 0.57 (0.10 a 1.13) |
| Cutter | 0.81 (−0.09 a 1.72) | 1.10 (0.19 a 2.18) |
| Slider | 0.08 (−0.31 a 0.47) | 0.54 (0.09 a 1.07) |
| Curva | 0.77 (0.16 a 1.40) | 0.68 (0.11 a 1.40) |
| Changeup | 0.65 (0.01 a 1.30) | 1.02 (0.23 a 1.82) |
| Splitter | 1.07 (−0.56 a 2.70) | 1.04 (0.16 a 2.16) |

b = 0.72 (0.48 a 0.95).

## Comparación con el Bayes empírico (`08`)
- Las medias posteriores casi no cambian: r = 0.95 entre ambos modelos; la media por tipo es igual salvo el splitter (2.8 → 2.2, solo 6 pitchers).
- **Los intervalos sí cambian, y ahora son creíbles.** Ancho mediano del intervalo de 80 %:

| Tipo | Bayes empírico | MCMC |
|---|---|---|
| Recta | 0.02 | 1.33 |
| Sinker | 0.02 | 1.64 |
| Slider | 0.05 | 1.52 |
| Curva | 0.01 | 2.10 |
| Cutter | 3.06 | 3.26 |
| Changeup | 3.18 | 2.77 |

- El hallazgo se mantiene pero se suaviza: changeup y cutter siguen siendo los tipos con más variación real entre pitchers (τ ≈ 1.0-1.1, contra 0.5-0.7 de los demás), aunque los intervalos de τ se traslapan. Lo honesto es decir "más evidencia de diferencias individuales en changeup y cutter", no "solo ahí importan".
- Ejemplo: changeup de pitcher_00904 (Diablos), 12.0 en crudo → 2.5 posterior (1.1 a 4.1), P(castigo > 3) = 0.26.
- Ningún pitcher-tipo tiene P(castigo > 3 carreras/100) > 0.8; 36 la tienen > 0.5. La regla del reporte ("si el rango completo queda arriba de 3") no la cumple nadie con MCMC; es mejor cambiarla a una probabilidad, por ejemplo "P(castigo > 3) > 50 %".

## Archivos
- `castigo_altitud_pitcher_tipo_mcmc.csv`: posterior por pitcher × tipo (media, p10, p90, P(castigo > 3)).
- `hiperparametros_mcmc.csv`, `convergencia.csv`, `autocorrelacion.csv`, `muestras_hiperparametros.csv.gz` (las 10,000 muestras de a, b y τ).
