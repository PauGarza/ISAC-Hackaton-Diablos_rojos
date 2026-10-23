"""EDA de los datos LMB para el modelo Stuff+: volumen, mezcla de pitcheos, calidad de datos y efecto de la altitud
por estadio sobre movimiento, velocidad, giro y resultados (datos crudos, sin modelo)."""
import numpy as np, pandas as pd

from pathlib import Path
RAIZ = Path(__file__).resolve().parents[2]
OUT = str(RAIZ / "results" / "eda") + "/"
d = pd.read_parquet(RAIZ / "data" / "stuff_model_df.parquet",
                    columns=["year", "game_anon_id", "pitcher_anon_id", "batter_anon_id", "altitude_category", "AutoPitchType",
                             "RelSpeed", "SpinRate", "InducedVertBreak", "HorzBreak", "PitcherThrows", "PitchCall", "hit_type",
                             "ExitSpeed", "Distance", "home_run", "is_swing", "is_whiff", "PlateLocHeight"])
j = pd.read_csv(RAIZ / "results" / "estadios" / "juegos_equipo_local.csv")
d = d.merge(j[["game_anon_id", "estadio", "altitud_m"]], on="game_anon_id", how="left")
d["hb"] = np.where(d.PitcherThrows == "Left", -d.HorzBreak, d.HorzBreak)  # zurdos espejados

# Volumen
pd.crosstab(d.year, d.altitude_category, margins=True).to_csv(OUT + "volumen_temporada_altitud.csv")
d.AutoPitchType.value_counts().rename("pitcheos").to_csv(OUT + "mezcla_pitcheos.csv")

# Por estadio
f = d[d.AutoPitchType == "Four-Seam"]
bip = d[d.PitchCall == "InPlay"]
g = d.groupby(["estadio", "altitud_m"]).agg(pitcheos=("year", "size"), swings=("is_swing", "sum"), wh=("is_whiff", "sum")).reset_index()
g["whiff_por_swing_%"] = 100 * g.wh / g.swings
g = g.merge(f.groupby("estadio").agg(ivb_recta=("InducedVertBreak", "mean"), hb_recta=("hb", "mean"),
                                     velo_recta=("RelSpeed", "mean"), spin_recta=("SpinRate", "mean")).reset_index(), on="estadio")
b = bip.groupby("estadio").agg(bip=("year", "size"), hr=("home_run", "sum"),
                               contacto_duro_pct=("ExitSpeed", lambda s: 100 * (s >= 95).mean())).reset_index()
fb = bip[bip.hit_type == "FlyBall"].groupby("estadio").Distance.mean().rename("distancia_elevado_pies").reset_index()
g = g.merge(b, on="estadio").merge(fb, on="estadio")
g["hr_por_bip_%"] = 100 * g.hr / g.bip
g = g.drop(columns=["swings", "wh"]).sort_values("altitud_m")
g.round(2).to_csv(OUT + "efecto_altitud_por_estadio.csv", index=False)
corr = {c: np.corrcoef(g.altitud_m, g[c])[0, 1] for c in ["ivb_recta", "hb_recta", "velo_recta", "spin_recta",
                                                          "whiff_por_swing_%", "contacto_duro_pct", "distancia_elevado_pies", "hr_por_bip_%"]}
pd.Series(corr, name="r_con_altitud").round(3).to_csv(OUT + "correlacion_con_altitud.csv")

# Por tipo: parques >=1,800 m vs <700 m
d["entorno"] = np.select([d.altitud_m >= 1800, d.altitud_m < 700], ["alto", "bajo"], "medio")
t = (d[d.AutoPitchType.isin(["Four-Seam", "Sinker", "Cutter", "Slider", "Curveball", "Changeup"]) & (d.entorno != "medio")]
     .groupby(["AutoPitchType", "entorno"]).agg(ivb=("InducedVertBreak", "mean"), hb=("hb", "mean"),
                                               velo=("RelSpeed", "mean"), spin=("SpinRate", "mean")).unstack().round(1))
t.columns = [f"{a}_{b}" for a, b in t.columns]
t.to_csv(OUT + "movimiento_por_tipo_alto_vs_bajo.csv")

# Calidad de datos
pd.Series({"pitcheos": len(d), "juegos": d.game_anon_id.nunique(), "pitchers": d.pitcher_anon_id.nunique(),
           "bateadores": d.batter_anon_id.nunique(), "sin_pitcher_id": int(d.pitcher_anon_id.isna().sum()),
           "sin_estadio": int(d.altitud_m.isna().sum()), "plateloc_height_0": int((d.PlateLocHeight == 0).sum())},
          name="valor").to_csv(OUT + "calidad_datos.csv")
print(g.round(2).to_string()); print(pd.Series(corr).round(3)); print(t)
