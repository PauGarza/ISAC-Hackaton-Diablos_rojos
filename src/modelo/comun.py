"""Rutas, constantes y constructores de features compartidos por todo el pipeline."""
import os
import numpy as np
import pandas as pd

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BASE = os.environ.get("MODELO_DIR", os.path.join(RAIZ, "outputs"))
DATOS = os.environ.get("DATOS_PARQUET", os.path.join(RAIZ, "data", "stuff_model_df.parquet"))
JUEGOS = os.environ.get("JUEGOS_CSV", os.path.join(RAIZ, "results", "estadios", "juegos_equipo_local.csv"))
TRABAJO = os.environ.get("TRABAJO_DIR", os.path.join(BASE, "intermedios"))
MODELOS = os.environ.get("MODELOS_DIR", os.path.join(RAIZ, "models"))
RESULTADOS = os.path.join(BASE, "resultados")

ALT_HARP_HELU = 2240.0
ALT_NIVEL_MAR = 0.0

# Clases de desenlace del pitcheo (modelo multiclase)
CLASES = ["ball", "called_strike", "whiff", "foul", "bip", "hbp"]

TIPOS_FB = ["Four-Seam", "Sinker", "Cutter"]
GRUPO_TIPO = {
    "Four-Seam": "FB", "Sinker": "FB", "Cutter": "FB",
    "Slider": "BRK", "Sweeper": "BRK", "Curveball": "BRK",
    "Changeup": "OFF", "Splitter": "OFF",
}

# Features de Stuff+: solo física de release/movimiento + arsenal + manos + entorno.
# Sin ubicación, sin count, sin etiqueta de tipo (H4: forma sobre etiqueta).
FEATS_STUFF = [
    "RelSpeed", "SpinRate", "spin_axis_m", "RelHeight", "rel_side_m", "Extension",
    "ivb", "hb_m", "mov_total", "mov_por_spin", "axis_dev",
    "velo_diff", "ivb_diff", "hb_diff", "axis_diff",
    "es_zurdo", "mismo_lado", "altitude_m",
]
# Location+: ubicación x count x manos x grupo de pitch. Sin física.
FEATS_LOC = [
    "PlateLocSide_m", "PlateLocHeight", "Balls", "Strikes", "es_zurdo", "mismo_lado",
    "grupo_FB", "grupo_BRK", "grupo_OFF", "altitude_m",
]
# Pitching+: todo junto + fatiga.
FEATS_PITCH = sorted(set(FEATS_STUFF) | set(FEATS_LOC)) + ["n_pitch_juego", "bat_enfrentados"]


def construir_features(df):
    """Agrega columnas derivadas (espejo de zurdos, movimiento, arsenal).

    Requiere: RelSpeed, SpinRate, SpinAxis, RelHeight, RelSide, Extension,
    InducedVertBreak, HorzBreak, PitcherThrows, BatterSide y, para el arsenal,
    fb_velo, fb_ivb, fb_hb, fb_axis (fastball primaria del pitcher en el mismo entorno).
    """
    out = df
    zurdo = (out["PitcherThrows"] == "Left").to_numpy()
    s = np.where(zurdo, -1.0, 1.0)
    out["es_zurdo"] = zurdo.astype(np.int8)
    out["mismo_lado"] = (out["PitcherThrows"] == out["BatterSide"]).astype(np.int8)
    out["hb_m"] = out["HorzBreak"] * s
    out["ivb"] = out["InducedVertBreak"]
    out["rel_side_m"] = out["RelSide"] * s
    out["spin_axis_m"] = np.where(zurdo, 360.0 - out["SpinAxis"], out["SpinAxis"])
    out["mov_total"] = np.hypot(out["hb_m"], out["ivb"])
    out["mov_por_spin"] = out["mov_total"] / (out["SpinRate"].clip(lower=300) / 1000.0)
    # Eje inferido por el movimiento (convención Trackman: 180 = backspin puro).
    eje_mov = (180.0 + np.degrees(np.arctan2(out["hb_m"], out["ivb"]))) % 360.0
    dev = (eje_mov - out["spin_axis_m"] + 180.0) % 360.0 - 180.0
    out["axis_dev"] = dev  # proxy de seam-shifted wake / spin no transversal
    if "fb_velo" in out:
        out["velo_diff"] = out["RelSpeed"] - out["fb_velo"]
        out["ivb_diff"] = out["ivb"] - out["fb_ivb"]
        out["hb_diff"] = out["hb_m"] - out["fb_hb"]
        out["axis_diff"] = (out["spin_axis_m"] - out["fb_axis"] + 180.0) % 360.0 - 180.0
    if "PlateLocSide" in out:
        out["PlateLocSide_m"] = out["PlateLocSide"] * s
    if "AutoPitchType" in out:
        g = out["AutoPitchType"].astype(str).map(GRUPO_TIPO).fillna("OTRO")
        out["grupo"] = g
        for k in ["FB", "BRK", "OFF"]:
            out[f"grupo_{k}"] = (g == k).astype(np.int8)
    return out


def escala_plus(xrv, media, sd):
    """xRV por pitcheo (carreras, + = bueno para el bateador) -> escala 100 + 10 z (alto = mejor pitcher)."""
    return 100.0 - 10.0 * (np.asarray(xrv) - media) / sd
