# Pipeline del modelo Stuff+

Se corre desde la raíz del repositorio, en este orden:

```
python src/modelo/01_preparar.py         # limpieza, turnos al bat, run values, features de arsenal -> outputs/intermedios/
python src/modelo/02_altitud_fisica.py   # k de traslado de movimiento por tipo de pitcheo (H1) -> models/k_altitud.json
python src/modelo/03_entrenar.py         # modelo de contacto + 15 LightGBM + escala -> models/
python src/modelo/05_scores.py           # scores por pitcheo, pitcher y arsenal; deltas de altitud; Diablos -> outputs/resultados/
python src/modelo/04_validar.py          # validación por temporada, parque y pitcher; H4
python src/modelo/06_estrategias.py      # rankings relativos y recomendaciones por pitcher
python src/modelo/07_validar_altitud.py  # efecto de altitud observado contra predicho
python src/modelo/09_rmse_calibracion.py # RMSE holdout y calibración por deciles
```

`05` va antes que `04` porque la validación usa los scores. Las salidas se escriben en `outputs/` (ignorado por git); la versión publicada de los resultados está en `results/`.

## Uso del modelo desde código

```python
from stuffplus import ModeloStuff          # con src/modelo en el path
m = ModeloStuff()
m.stuff_plus(pitch_dict, altitud_destino=2240, altitud_medicion=0)
```

- Stuff+ usa `models/stuff_clase.txt` (multiclase; clases en `comun.CLASES`) y `models/stuff_bip_xrv.txt` (regresión), con las features `comun.FEATS_STUFF` en ese orden.
- xRV = Σ_{c≠bip} p_c·rv_medio_clase[c] + p_bip·(bip_xrv − v_count_medio_bip). Las constantes están en `models/escala.json`.
- Stuff+ = 100 − 10·(xRV − media)/sd.
- Traslado entre altitudes: IVB/HB × exp(−k_tipo·(alt_destino − alt_medicion)/1000), con k en `models/k_altitud.json`.
