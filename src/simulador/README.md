# Simulador Stuff+ Harp Helú

`construir_motor_final.py` exporta los modelos `models/stuff_clase.txt` (multiclase) y `models/stuff_bip_xrv.txt` (regresión) a `app/simulador/motor.json`, en un formato compacto de árboles (`[feature, umbral, default_left, izq, der]`) que el navegador evalúa sin servidor. Se verificó contra `ModeloStuff.stuff_plus` (`src/modelo/stuffplus.py`) en 24 casos, con diferencia 0.00.

Requiere haber corrido el pipeline (`outputs/resultados/scores_pitch.parquet` y `delta_altitud_por_tipo.csv`). De `motor_provisional.json` (el motor de una versión anterior) toma los ajustes de traslado de movimiento entre entornos.

```
python src/simulador/construir_motor_final.py
```

La app es `app/simulador/simulador_standalone.html`: un solo archivo, funciona sin internet.
