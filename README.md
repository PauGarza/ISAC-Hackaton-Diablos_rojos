# Stuff+ LMB: calidad de pitcheo ajustada por entorno

**2026 ISAC Hackathon · Diablos Rojos del México**

Equipo: Paulina Garza Allende, Othoniel Reyes Camacho, Andrea Guerra y Jose Rodrigo Dumas Avalos

---

## Resumen

A 2,240 metros el aire es cerca de 20 % menos denso, y eso le quita al pitcheo el movimiento que produce la fuerza Magnus. Construimos un modelo **Stuff+** para la LMB con 629,616 pitcheos Trackman de 2024 a 2026. Son 15 modelos LightGBM que predicen por separado la probabilidad de swing y fallo, strike cantado, rodado, contacto duro y out, y convierten esas probabilidades a carreras esperadas. De ahí salen tres métricas: **Stuff+** (solo la física del pitcheo), **Location+** (ubicación y cuenta) y **Pitching+** (las dos juntas). El modelo usa la altitud como variable, así que el mismo pitcheo se puede evaluar al nivel del mar y en el Estadio Alfredo Harp Helú.

Encima del LightGBM, un **modelo bayesiano jerárquico (MCMC, PyMC/NUTS)** estima cuánto pierde cada pitcher en altura, con su rango de incertidumbre. Con ambos definimos el perfil ideal del pitcher Diablos, armamos recomendaciones de reclutamiento y construimos un simulador interactivo.

## Resultados principales

| | |
|---|---|
| Validación fuera de muestra (entrena 2024–25, pronostica 2026) | Pitching+ r = **0.56** con las carreras permitidas por pitcher, contra −0.26 de la referencia del reto |
| Estabilidad año a año | Stuff+ r = 0.61–0.68, contra 0.23–0.29 de la efectividad |
| Efecto de la altitud por tipo de pitcheo | La recta pierde 4.8" de bote y 22 puntos de Stuff+; el slider solo 9 |
| Hipótesis del reto | H1, H3 y H4 se confirman; H2 (el changeup gana valor en altura) no: en el Harp Helú casi duplica sus jonrones |
| Mejor arsenal para el Harp Helú | Cutter + slider: 98 al nivel del mar, 115 en altura |

Escala de todos los scores: 100 + 10·z (100 = promedio de la liga, 110 = arriba del 84 %, 120+ = élite). Stuff+ − 50 = grado de scout (20–80).

## Empieza aquí (para los jueces)

| Qué | Archivo |
|---|---|
| Resumen ejecutivo | [`reports/resumen_ejecutivo/reporte_conclusiones.pdf`](reports/resumen_ejecutivo/reporte_conclusiones.pdf) |
| Reporte completo para dirección deportiva | [`reports/reporte_final_diablos.pdf`](reports/reporte_final_diablos.pdf) |
| Documento técnico del modelo | [`docs/documento_tecnico_stuffplus.pdf`](docs/documento_tecnico_stuffplus.pdf) |
| Simulador Harp Helú vs nivel del mar | En línea: https://claude.ai/artifact/KYU5KNKmTSzew9CFQMMRhd · Local: [`app/simulador/simulador_standalone.html`](app/simulador/simulador_standalone.html) (descargar y abrir; funciona sin internet). **Ambos contienen el mismo simulador.** |
| Scores por pitcher y arsenal | [`results/scores/`](results/scores/) |

## Estructura del repositorio

```
├── app/simulador/           Simulador standalone (HTML) y motor exportado del modelo
├── data/                    Datos crudos (no incluidos, ver data/README.md)
├── docs/                    Documento técnico, bases del reto, identificación de estadios, notas
├── models/                  Modelos LightGBM entrenados y constantes de escala
├── notebooks/               EDA: calidad de datos, entorno y altitud, run values, hipótesis
├── reports/
│   ├── reporte_final_diablos.{pdf,html}   Reporte completo (5 reportes + anexos)
│   ├── resumen_ejecutivo/                 Conclusiones en un solo documento
│   ├── directivos/                        Cada reporte por separado (md, html, pdf) y sus gráficas
│   └── eda/                               Reportes exploratorios
├── results/
│   ├── scores/              Stuff+, Location+ y Pitching+ por pitcher, temporada, arsenal y estadio; SHAP
│   ├── diablos/             Staff de Diablos, perfil ideal, top 30 de la liga para el Harp Helú
│   ├── validacion/          Holdout, estabilidad, calibración, pruebas de H1 y H3
│   ├── bayes_mcmc/          Castigo de altitud por pitcher × tipo, convergencia y muestras
│   ├── eda/                 Tablas del EDA por estadio
│   └── estadios/            Equipo local y estadio inferidos por juego
└── src/
    ├── modelo/              Pipeline Stuff+ 01→09 (ver src/modelo/README.md)
    ├── bayes/               Modelo jerárquico: Bayes empírico (08) y MCMC (09)
    ├── eda/                 Scripts del EDA
    ├── reportes/            Gráficas y construcción de reportes (md → html → pdf)
    ├── simulador/           Exportación del modelo al simulador
    └── data_prep.py, viz.py Funciones usadas por los notebooks
```

## Reproducir

```bash
pip install -r requirements.txt
# copiar stuff_model_df.parquet a data/
python src/modelo/01_preparar.py      # y así hasta 09, ver src/modelo/README.md
python src/bayes/09_bayes_mcmc.py
```

Las salidas del pipeline van a `outputs/` (ignorado por git). La versión publicada y la que usan los reportes está en `results/`.

## Notas y limitaciones

- **Estadios y equipos inferidos.** Los datos no traen el estadio ni el equipo; los inferimos por récord y altitud (ver [`docs/identificacion_harp_helu.md`](docs/identificacion_harp_helu.md)). No los ha confirmado ISAC.
- **IDs anonimizados** tal como vienen en los datos.
- **Datos no publicados.** Ni los datos crudos ni los scores por pitcheo están en el repo; todo lo que hay en `results/` son agregados.
- Las tablas `results/scores/shap_*.csv`, `riesgo_contacto_duro_hr.csv` y `arsenal_combinaciones_harp_helu.csv` se generaron en sesiones de análisis cuyo script no está en este repositorio.

## Referencias, herramientas y uso de IA

- Nathan, A. M. (2008). The effect of spin on the flight of a baseball. *American Journal of Physics*, 76(2).
- Richardson, E. (2014). High Altitude Offense. *Baseball Research Journal*, SABR.
- Deshpande, S. K. y Wyner, A. J. (2017). A hierarchical Bayesian model of pitch framing. arXiv:1704.00823.
- Hoffman, M. D. y Gelman, A. (2014). The No-U-Turn Sampler. *JMLR*, 15.
- Ke, G. et al. (2017). LightGBM: A highly efficient gradient boosting decision tree. *NeurIPS* 30.
- Lundberg, S. M. y Lee, S.-I. (2017). A unified approach to interpreting model predictions (SHAP). *NeurIPS* 30.
- Software: Python, pandas, scikit-learn, LightGBM, PyMC 5, ArviZ, matplotlib.
- **IA generativa:** usamos Claude Code (Anthropic) como apoyo para programar el análisis y el simulador, revisar la congruencia entre resultados y reportes, y redactar y editar los reportes. Las decisiones de modelado y las conclusiones son del equipo.

Lista completa en [`reports/directivos/md/06_referencias.md`](reports/directivos/md/06_referencias.md).
