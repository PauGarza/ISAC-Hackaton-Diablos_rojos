---
numero: 6
etiqueta: B
titulo: Referencias
pregunta: Las fuentes, los datos y las herramientas detrás de estos reportes.
---

## Física de la altitud y béisbol

- Nathan, A. M. (2008). The effect of spin on the flight of a baseball. *American Journal of Physics*, 76(2), 119–124.
- Richardson, E. (2014). High Altitude Offense. *Baseball Research Journal*, SABR.

## Métodos estadísticos

- Deshpande, S. K. y Wyner, A. J. (2017). A hierarchical Bayesian model of pitch framing. arXiv:1704.00823.
- Brill, R. S., Deshpande, S. K. y Wyner, A. J. (2022). A Bayesian analysis of the time through the order penalty in baseball. arXiv:2210.06724.
- Hoffman, M. D. y Gelman, A. (2014). The No-U-Turn Sampler: adaptively setting path lengths in Hamiltonian Monte Carlo. *Journal of Machine Learning Research*, 15, 1593–1623.
- Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q. y Liu, T.-Y. (2017). LightGBM: A highly efficient gradient boosting decision tree. *Advances in Neural Information Processing Systems*, 30.
- Lundberg, S. M. y Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems*, 30.

## Software

- LightGBM (modelos Stuff+, Location+ y Pitching+), pandas y scikit-learn, en Python.
- PyMC 5 y ArviZ (modelo bayesiano jerárquico, estimado con MCMC por el muestreador NUTS).

## Datos

- ISAC y Diablos Rojos del México (2026). Datos pitcheo a pitcheo de la Liga Mexicana de Béisbol, temporadas 2024 a 2026 (TrackMan), con identificadores anonimizados. Proporcionados para el 2026 ISAC Hackathon.
- ISAC (2026). *2026 ISAC Hackathon – Diablos Rojos: Stuff Plus Model, Calidad de Pitcheo Ajustada por Entorno*. Bases del reto, de donde salen la escala Stuff+, las hipótesis H1 a H4 y los entregables.
- Datos públicos de Grandes Ligas de Jacob Misiorowski y Chad Patrick, usados solo como ejemplo en el reporte 3 y en el anexo A. Las entradas son aproximadas: el giro, el eje y el movimiento horizontal los estimamos nosotros.

## Herramientas de inteligencia artificial

- Anthropic (2026). *Claude Code* [asistente de inteligencia artificial]. https://claude.com/claude-code. Lo usamos como apoyo para programar el análisis y el simulador, revisar la congruencia entre resultados y reportes, y redactar y editar los reportes.
- El simulador en línea está publicado como artifact de Claude (claude.ai).
