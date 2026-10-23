# Modelo bayesiano jerárquico: cómo se implementó y cómo leerlo

Código: `entregables/06_codigo/bayes/08_bayes_jerarquico.py`. Resultados: `03_validacion_hipotesis/castigo_altitud_pitcher_tipo.csv` y `hiperparametros.csv`.

## 1. La pregunta

¿Cuántas carreras extra por 100 pitcheos le cuesta a **este** pitcher lanzar **este** tipo de pitcheo en altura? El dato crudo es ruidoso: un pitcher con 50 changeups en altura puede verse desastroso o inmune por pura suerte. El modelo jerárquico separa la señal del ruido.

## 2. El dato

Para cada combinación pitcher × tipo de pitcheo *j* con al menos 30 pitcheos en parques de 1,800 m o más y 30 en parques de menos de 700 m:

- **d_j** = RV/100 observado en altura − RV/100 observado abajo (positivo = peor en altura).
- **se_j** = error estándar de esa diferencia = 100 · σ_pitcheo · √(1/n_alto + 1/n_bajo).

Hay 1,186 combinaciones con datos en ambos entornos, de 5,905 en total.

## 3. Las distribuciones (parte teórica)

Es un modelo normal-normal de tres niveles:

**Nivel 1, dato (verosimilitud):**
d_j ~ Normal(θ_j, se_j²)
θ_j es el castigo *verdadero* del pitcheo; d_j es lo que vimos, con ruido de muestreo conocido.

**Nivel 2, pitcher dentro de su tipo (prior):**
θ_j ~ Normal(a_t + b · pred_j, τ_t²)
- pred_j = castigo que predice el LightGBM por la forma del pitcheo (−Δ Stuff+ Harp Helú vs mar, convertido a carreras: 10 puntos = 1.26 carreras/100).
- a_t = ajuste propio de cada tipo de pitcheo *t* (recta, sinker, cutter, slider, curva, changeup, splitter).
- τ_t = cuánto varían de verdad los pitchers entre sí dentro de ese tipo, más allá de lo que explica la forma.

**Nivel 3, liga (hiperparámetros):**
b es común a toda la liga y conecta la física del LightGBM con lo observado. a_t y τ_t son uno por tipo.

## 4. Cómo se estimó (software)

- **Python** con numpy, pandas y scipy. No se usó Stan, PyMC ni MCMC.
- Es **Bayes empírico**: los hiperparámetros (a_t, b, τ_t) se estiman maximizando la verosimilitud marginal, en la que θ_j se integra analíticamente:
  d_j ~ Normal(a_t + b · pred_j, τ_t² + se_j²)
  La optimización usa `scipy.optimize.minimize` con L-BFGS-B, sobre log τ para que τ sea positivo.
- Con los hiperparámetros fijos, la posterior de cada θ_j es **exacta y cerrada** (normal-normal conjugada):
  - precisión posterior = 1/τ_t² + 1/se_j²
  - media posterior = (prior/τ_t² + d_j/se_j²) / precisión
  - **peso de los datos** = τ_t² / (τ_t² + se_j²); qué tanto se cree la historia del pitcher contra el promedio de su tipo y forma.
- Pitchers sin datos en ambos entornos reciben la predictiva previa: a_t + b · pred_j ± τ_t.
- Intervalo de 80 %: media ± 1.2816 · √(varianza posterior).

Es el mismo enfoque de Deshpande y Wyner (2017) para el framing de catchers.

## 5. Qué salió (hiperparámetros)

| Tipo | a_t | τ_t (carreras/100) | Pitcher-tipo con datos | Peso medio de los datos | Ancho mediano del intervalo 80 % |
|---|---|---|---|---|---|
| Recta | 0.08 | 0.006 | 404 | 0.00 | 0.02 |
| Sinker | 0.63 | 0.008 | 200 | 0.00 | 0.02 |
| Cutter | 1.05 | **1.23** | 41 | 0.07 | **3.2** |
| Slider | 0.19 | 0.019 | 299 | 0.00 | 0.05 |
| Curva | 0.96 | 0.003 | 99 | 0.00 | 0.01 |
| Changeup | 0.88 | **1.29** | 137 | 0.09 | **3.3** |
| Splitter | 1.92 | 0.003 | 6 | 0.00 | 0.01 |

b = 0.61 (común): por cada carrera de castigo que predice el LightGBM, en la realidad se ven ~0.6, más el ajuste del tipo.

## 6. Interpretación para decidir

**Lectura principal.** En recta, sinker, slider y curva τ ≈ 0: una vez que sabes el tipo y la forma del pitcheo, la historia del pitcher en altura no agrega información. Todo lo que se ve de diferencia entre pitchers es ruido de muestra. **Decisión:** para esos pitcheos, evalúa a un prospecto con el simulador (forma) y no con sus números en parques altos.

**Excepciones: changeup y cutter.** τ ≈ 1.2-1.3 carreras/100: sí hay pitchers que aguantan la altura mejor que otros con la misma forma. **Decisión:** si el arma de un prospecto es changeup o cutter, revisa su castigo posterior.

Ejemplos reales de changeup (columna `castigo_post`, intervalo p10-p90):

| Pitcher | Crudo | Predicho por forma | Posterior | Rango 80 % | Peso de los datos |
|---|---|---|---|---|---|
| pitcher_00737 (Piratas, 380/601 pitcheos) | −1.0 | 1.3 | **0.7** | −0.6 a 2.1 | 35 % |
| pitcher_00767 (Pericos, 388/329) | 7.0 | 2.0 | **3.5** | 2.1 a 4.9 | 29 % |
| pitcher_00904 (Diablos, 51/67) | 12.0 | 1.8 | **2.6** | 1.0 a 4.2 | 6 % |

Con muestra grande, el modelo le cree más al pitcher; con poca muestra (00904) lo jala hacia lo que predice su forma. Regla operativa del reporte: si el rango completo queda arriba de 3 carreras/100, ese pitcheo no debe ser su arma en casa.

## 7. Limitaciones que hay que decir si preguntan

1. **Es Bayes empírico, no totalmente bayesiano.** Los hiperparámetros se fijan en su estimado puntual, así que los intervalos no incluyen la incertidumbre de a_t, b y τ_t. Por eso en los tipos con τ ≈ 0 el intervalo mide casi nada (0.01-0.05 carreras): eso **no** significa que conozcamos el castigo con esa precisión, sino que el modelo no ve variación entre pitchers. Con MCMC (PyMC o Stan) esos intervalos serían más anchos. Para decidir, solo los intervalos de changeup y cutter son informativos.
2. La correlación entre el castigo crudo y el predicho por forma es baja (r = 0.09): el dato pitcher por pitcher es muy ruidoso, que es justo el motivo de usar el modelo.
3. Altura definida por umbrales (≥1,800 m vs <700 m); los parques intermedios no entran al dato observado.
4. El splitter tiene solo 6 combinaciones con datos: su estimado es casi todo prior.
