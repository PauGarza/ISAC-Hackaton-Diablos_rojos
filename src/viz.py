"""Estilo común para las figuras del EDA (paleta validada para daltonismo)."""

from pathlib import Path

import matplotlib.pyplot as plt

from .data_prep import ALTITUDE_ORDER, ROOT

FIG_DIR = ROOT / "reports" / "figures"

# Altitud = variable ordinal -> una sola tinta (azul), de claro a oscuro
ALT_COLORS = dict(zip(ALTITUDE_ORDER, ["#86b6ef", "#2a78d6", "#104281"]))
ALT_LABELS = {"No Altitude": "Sin altitud", "Medium Altitude": "Altitud media", "Extreme Altitude": "Altitud extrema"}
# Categórico (máx. 3 series por gráfica)
CAT = ["#2a78d6", "#eb6834", "#1baf7a"]
INK, INK2, MUTED, GRID, AXIS = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
PITCH_ORDER = ["Four-Seam", "Sinker", "Cutter", "Slider", "Curveball", "Changeup", "Splitter"]


def set_style():
    plt.rcParams.update({
        "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "savefig.facecolor": "#fcfcfb",
        "axes.edgecolor": AXIS, "axes.labelcolor": INK2, "axes.titlecolor": INK,
        "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.labelsize": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
        "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelsize": 9, "ytick.labelsize": 9,
        "lines.linewidth": 2, "lines.markersize": 7, "legend.frameon": False, "legend.fontsize": 9,
        "font.family": ["Segoe UI", "DejaVu Sans", "sans-serif"], "figure.dpi": 110,
    })


def savefig(fig, name):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    path = Path(FIG_DIR) / f"{name}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    return path
