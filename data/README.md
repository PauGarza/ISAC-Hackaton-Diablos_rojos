# Datos

Los datos Trackman de la LMB (2024–2026) son propiedad de ISAC / Diablos Rojos y **no se incluyen en este repositorio**.

Para reproducir el pipeline, coloca aquí el archivo entregado por los organizadores:

```
data/
└── stuff_model_df.parquet      # 629,616 pitcheos, IDs anonimizados
```

Las rutas se pueden cambiar con variables de entorno (ver `src/modelo/comun.py`): `DATOS_PARQUET`, `JUEGOS_CSV`, `MODELO_DIR`, `MODELOS_DIR`.

Los scores por pitcheo (`scores_pitch_*.csv.gz`) tampoco se publican porque incluyen las variables Trackman originales; se regeneran con `src/modelo/05_scores.py`.
