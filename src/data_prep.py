"""Limpieza y features compartidas para el EDA y el modelo Stuff+ (Hackathon ISAC 2026 - Diablos Rojos).

Uso típico:
    from src.data_prep import build_dataset
    df, re_table = build_dataset()

Convenciones:
- `delta_run_exp` está en perspectiva del BATEADOR (positivo = bueno para la ofensiva), igual que Statcast.
  Para el pitcher, un valor negativo es bueno.
- `hb_arm` / `rel_side_arm`: movimiento horizontal y release normalizados al lado del brazo del pitcher
  (positivo = hacia el lado del brazo), para comparar zurdos y derechos en la misma escala.
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "stuff_model_df.parquet"
PROCESSED_PATH = ROOT / "data" / "processed" / "pitches_eda.parquet"

ALTITUDE_ORDER = ["No Altitude", "Medium Altitude", "Extreme Altitude"]
PITCH_TYPE_MAP = {
    "Four-Seam": "Four-Seam",
    "Sinker": "Sinker",
    "TwoSeamFastBall": "Sinker",
    "OneSeamFastBall": "Sinker",
    "Cutter": "Cutter",
    "Slider": "Slider",
    "Sweeper": "Slider",  # solo existe desde 2025: se agrupa con Slider y se conserva el flag is_sweeper_label
    "Curveball": "Curveball",
    "Changeup": "Changeup",
    "Splitter": "Splitter",
    # Other / Knuckleball quedan como NaN (muestra insignificante)
}
FASTBALLS = ["Four-Seam", "Sinker"]
SWING_CALLS = ["StrikeSwinging", "FoulBall", "FoulBallNotFieldable", "FoulBallFieldable", "InPlay"]
STUFF_PHYSICS = [
    "RelSpeed", "SpinRate", "SpinAxis", "InducedVertBreak", "HorzBreak",
    "RelHeight", "RelSide", "Extension",
]


def load_raw(path=RAW_PATH):
    return pd.read_parquet(path)


def clean(df):
    """Tipos, orden de las filas, pitch types, flags de calidad y variables derivadas.

    No elimina filas: marca problemas con columnas `flag_*` y resume en `usable_stuff`.
    """
    df = df.copy()
    df["row_order"] = np.arange(len(df))

    # Orden: los juegos vienen contiguos, pero ~5% tiene entradas desordenadas.
    # Orden estable por (juego, entrada, alta/baja) conservando el orden original dentro de cada media entrada.
    game_order = pd.Series(pd.factorize(df["game_anon_id"])[0], index=df.index)
    half = df["Top/Bottom"].astype(str).map({"Top": 0, "Bottom": 1})
    df = (
        df.assign(_g=game_order, _h=half)
        .sort_values(["_g", "Inning", "_h", "row_order"], kind="mergesort")
        .drop(columns=["_g", "_h"])
        .reset_index(drop=True)
    )

    df["EffectiveVelo"] = pd.to_numeric(df["EffectiveVelo"], errors="coerce")
    for c in ["Inning", "Outs", "Balls", "Strikes", "OutsOnPlay", "RunsScored"]:
        df[c] = df[c].astype("Int64")

    # Mano del pitcher: completar None/Undefined con la moda del pitcher
    throws = df["PitcherThrows"].where(df["PitcherThrows"].isin(["Right", "Left"]))
    mode = throws.groupby(df["pitcher_anon_id"]).agg(lambda s: s.mode().iat[0] if s.notna().any() else np.nan)
    df["PitcherThrows"] = throws.fillna(df["pitcher_anon_id"].map(mode))
    df["BatterSide"] = df["BatterSide"].where(df["BatterSide"].isin(["Right", "Left"]))

    # Pitch types
    raw_pt = df["AutoPitchType"].astype(str)
    df["pitch_type"] = raw_pt.map(PITCH_TYPE_MAP)
    df["is_sweeper_label"] = raw_pt.eq("Sweeper")

    df["altitude_category"] = pd.Categorical(df["altitude_category"], categories=ALTITUDE_ORDER, ordered=True)
    df["altitude_level"] = df["altitude_category"].cat.codes.replace(-1, np.nan)

    # Variables derivadas
    arm = np.where(df["PitcherThrows"].eq("Left"), -1.0, 1.0)
    df["hb_arm"] = df["HorzBreak"] * arm
    df["rel_side_arm"] = df["RelSide"] * arm
    df["total_movement"] = np.hypot(df["InducedVertBreak"], df["HorzBreak"])
    df["speed_drop_pct"] = (df["RelSpeed"] - df["ZoneSpeed"]) / df["RelSpeed"]
    df["spin_per_mph"] = df["SpinRate"] / df["RelSpeed"]  # "Bauer units"
    df["same_side"] = df["PitcherThrows"].eq(df["BatterSide"])

    # Flags de resultado reconstruidos desde PitchCall (las columnas is_* originales traen inconsistencias,
    # p. ej. 463 BallCalled con is_swing = 1)
    call = df["PitchCall"].astype(str)
    df["swing"] = call.isin(SWING_CALLS)
    df["whiff"] = call.eq("StrikeSwinging")
    df["called_strike"] = call.eq("StrikeCalled")
    df["csw"] = df["whiff"] | df["called_strike"]
    df["in_play"] = call.eq("InPlay")
    df["in_zone"] = df["in_strike_zone"].eq(1)
    df["chase"] = df["swing"] & ~df["in_zone"]

    # Flags de calidad
    df["flag_undefined_call"] = call.eq("Undefined")
    df["flag_loc_sentinel"] = df["PlateLocHeight"].eq(0)
    df["flag_bad_extension"] = ~df["Extension"].between(3, 9)
    df["flag_movement_outlier"] = (df["InducedVertBreak"].abs() > 35) | (df["HorzBreak"].abs() > 35)
    df["flag_release_outlier"] = ~df["RelHeight"].between(2, 8)
    df["flag_missing_physics"] = df[STUFF_PHYSICS].isna().any(axis=1)
    df["flag_no_altitude"] = df["altitude_category"].isna()
    df["flag_no_pitch_type"] = df["pitch_type"].isna()
    flags = [c for c in df.columns if c.startswith("flag_")]
    df["usable_stuff"] = ~df[flags].any(axis=1) & df["PitcherThrows"].notna()
    return df


def add_sequence_ids(df):
    """Reconstruye media entrada, turno al bat (PA), número de pitch, pitch previo y veces en el orden."""
    df = df.copy()
    half = df["Top/Bottom"].astype(str)
    df["half_inning_id"] = df["game_anon_id"] + "_" + df["Inning"].astype(str) + half.str[0]

    terminal = df["PitchCall"].astype(str).isin(["InPlay", "HitByPitch"]) | df["KorBB"].ne("Undefined")
    new_hi = df["half_inning_id"].ne(df["half_inning_id"].shift())
    new_batter = df["batter_anon_id"].ne(df["batter_anon_id"].shift())
    prev_terminal = terminal.shift(fill_value=True)
    df["pa_terminal"] = terminal
    df["pa_id"] = (new_hi | new_batter | prev_terminal).cumsum()

    df["pitch_num_pa"] = df.groupby("pa_id").cumcount() + 1
    df["pitch_num_game_pitcher"] = df.groupby(["game_anon_id", "pitcher_anon_id"]).cumcount() + 1
    df["prev_pitch_type"] = df.groupby("pa_id")["pitch_type"].shift().fillna("None")

    pa_first = df["pitch_num_pa"].eq(1)
    tto = pa_first.astype(int).groupby([df["game_anon_id"], df["pitcher_anon_id"], df["batter_anon_id"]]).cumsum()
    df["times_through_order"] = tto.clip(lower=1)
    return df


def _state_cols(df):
    return [df["Outs"].astype(int), df["Balls"].astype(int), df["Strikes"].astype(int)]


def run_expectancy_table(df, by=None):
    """RE(outs, bolas, strikes): carreras promedio desde antes del pitch hasta el final de la media entrada.

    No hay corredores en base en los datos, así que la tabla promedia sobre todos los estados de bases.
    Se excluyen las bajas de la 9ª entrada o posteriores (walk-offs truncan la media entrada).
    """
    keys = ["Outs", "Balls", "Strikes"] + ([by] if by else [])
    d = df[keys + ["half_inning_id", "Inning", "Top/Bottom", "RunsScored"]].copy()
    runs = d["RunsScored"].fillna(0).astype(float)
    d["runs_rest"] = runs[::-1].groupby(d["half_inning_id"][::-1]).cumsum()[::-1]
    keep = ~((d["Inning"] >= 9) & d["Top/Bottom"].astype(str).eq("Bottom"))
    keep &= d["Outs"].between(0, 2) & d["Balls"].between(0, 3) & d["Strikes"].between(0, 2)
    return (
        d[keep].groupby(keys, observed=True)["runs_rest"]
        .agg(re="mean", n="size").reset_index()
    )


def add_run_value(df, re_table=None, by=None):
    """Agrega `re_before`, `re_after` y `delta_run_exp` (perspectiva del bateador).

    delta_run_exp = RE(estado siguiente) - RE(estado actual) + carreras anotadas en el pitch.
    El estado siguiente es el del próximo pitch de la misma media entrada; si es el último pitch, RE = 0.
    """
    df = df.copy()
    if re_table is None:
        re_table = run_expectancy_table(df, by=by)
    keys = ["Outs", "Balls", "Strikes"] + ([by] if by else [])
    lookup = re_table.set_index(keys)["re"]

    idx_now = pd.MultiIndex.from_frame(df[keys])
    df["re_before"] = lookup.reindex(idx_now).to_numpy()

    nxt = df[keys].shift(-1)
    same_hi = df["half_inning_id"].eq(df["half_inning_id"].shift(-1))
    nxt.loc[~same_hi] = np.nan
    valid = nxt.notna().all(axis=1)
    re_after = pd.Series(0.0, index=df.index)
    re_after[valid] = lookup.reindex(pd.MultiIndex.from_frame(nxt[valid].astype(df[keys].dtypes.to_dict()))).to_numpy()
    df["re_after"] = re_after
    df["delta_run_exp"] = df["re_after"] - df["re_before"] + df["RunsScored"].fillna(0).astype(float)
    return df, re_table


def add_arsenal_features(df, min_fb=20):
    """Features relacionales respecto al fastball principal del pitcher.

    El fastball de referencia se calcula por (pitcher, temporada, altitud) cuando hay al menos `min_fb`
    fastballs en ese ambiente; si no, por (pitcher, temporada). Así un slider en CDMX se compara contra
    el fastball lanzado en el mismo tipo de aire.
    """
    df = df.copy()
    base = df[df["usable_stuff"]]
    usage = base.groupby(["pitcher_anon_id", "year", "pitch_type"]).size()
    df["pitch_usage_pct"] = (
        df.set_index(["pitcher_anon_id", "year", "pitch_type"]).index.map(
            (usage / usage.groupby(level=[0, 1]).transform("sum")).to_dict()
        )
    )

    fb_stats = ["RelSpeed", "InducedVertBreak", "hb_arm", "RelHeight", "rel_side_arm"]
    fbs = base[base["pitch_type"].isin(FASTBALLS)]
    # fastball principal = el fastball más usado por pitcher-temporada
    main_fb = (
        fbs.groupby(["pitcher_anon_id", "year", "pitch_type"]).size()
        .reset_index(name="n").sort_values("n").groupby(["pitcher_anon_id", "year"]).tail(1)
        [["pitcher_anon_id", "year", "pitch_type"]].rename(columns={"pitch_type": "primary_fb"})
    )
    fbs = fbs.merge(main_fb, on=["pitcher_anon_id", "year"])
    fbs = fbs[fbs["pitch_type"] == fbs["primary_fb"]]

    by_env = fbs.groupby(["pitcher_anon_id", "year", "altitude_category"], observed=True)[fb_stats].agg(["median", "size"])
    env_ok = by_env[(fb_stats[0], "size")] >= min_fb
    by_env = by_env.loc[env_ok, [(c, "median") for c in fb_stats]]
    by_env.columns = [f"fb_{c}" for c in fb_stats]
    by_season = fbs.groupby(["pitcher_anon_id", "year"])[fb_stats].median().add_prefix("fb_")

    df = df.merge(main_fb, on=["pitcher_anon_id", "year"], how="left")
    env = df[["pitcher_anon_id", "year", "altitude_category"]].merge(
        by_env.reset_index(), on=["pitcher_anon_id", "year", "altitude_category"], how="left"
    )
    season = df[["pitcher_anon_id", "year"]].merge(by_season.reset_index(), on=["pitcher_anon_id", "year"], how="left")
    for c in by_season.columns:
        df[c] = env[c].fillna(season[c]).to_numpy()

    df["velo_diff_vs_fb"] = df["RelSpeed"] - df["fb_RelSpeed"]
    df["ivb_diff_vs_fb"] = df["InducedVertBreak"] - df["fb_InducedVertBreak"]
    df["hb_diff_vs_fb"] = df["hb_arm"] - df["fb_hb_arm"]
    df["release_dist_vs_fb"] = np.hypot(df["RelHeight"] - df["fb_RelHeight"], df["rel_side_arm"] - df["fb_rel_side_arm"])
    return df


def add_air_density(df, min_pitches=15):
    """Densidad relativa del aire por juego, estimada con el arrastre.

    El arrastre es proporcional a la densidad, así que la fracción de velocidad perdida entre release y home
    (speed_drop_pct) de los four-seam funciona como "barómetro". Se normaliza contra la mediana de los juegos
    'No Altitude' (que no es exactamente nivel del mar).
    Ojo: diferencias de calibración de Trackman entre parques también entran en esta medida.
    """
    df = df.copy()
    ff = df[df["usable_stuff"] & df["pitch_type"].eq("Four-Seam")]
    g = ff.groupby("game_anon_id")["speed_drop_pct"].agg(["median", "size"])
    g = g[g["size"] >= min_pitches]["median"]
    games_alt = df.drop_duplicates("game_anon_id").set_index("game_anon_id")["altitude_category"]
    ref = g[games_alt.reindex(g.index).eq("No Altitude")].median()
    df["game_speed_drop_pct"] = df["game_anon_id"].map(g)
    df["air_density_ratio"] = df["game_speed_drop_pct"] / ref
    return df


def _mode(s):
    m = s.dropna().mode()
    return m.iat[0] if len(m) else np.nan


def add_park_ids(df, resolution=1.0, min_home_games=10, min_jaccard=0.08, seed=0):
    """Reconstruye el equipo local de cada juego y lo enlaza entre temporadas -> `park_id`.

    El dataset no trae estadio. Pero en la parte ALTA de cada entrada lanza el equipo LOCAL, así que:
    1. Por temporada, se arma un grafo de pitchers que lanzan del mismo lado en el mismo juego y se
       detectan comunidades (Louvain) ~ equipos.
    2. El equipo local de un juego es la comunidad más frecuente entre los pitchers de la parte alta.
    3. Los equipos se enlazan entre temporadas por coincidencia de pitchers (Jaccard, mejor match mutuo).
    Resultado: `home_team_season` y `park_id` (franquicia local ~ estadio). Es una INFERENCIA: confirmar con ISAC.
    """
    import networkx as nx
    from itertools import combinations

    d = df.dropna(subset=["pitcher_anon_id"])
    d = d.assign(home_side=d["Top/Bottom"].astype(str).eq("Top"))
    d = d.drop_duplicates(["game_anon_id", "home_side", "pitcher_anon_id"])

    home_team, members, n_home = {}, {}, {}
    for yr, dy in d.groupby("year"):
        G = nx.Graph()
        G.add_nodes_from(dy["pitcher_anon_id"].unique())
        for _, grp in dy.groupby(["game_anon_id", "home_side"]):
            for a, b in combinations(sorted(grp["pitcher_anon_id"]), 2):
                w = G.get_edge_data(a, b, {"weight": 0})["weight"]
                G.add_edge(a, b, weight=w + 1)
        comms = nx.community.louvain_communities(G, weight="weight", resolution=resolution, seed=seed)
        team = {p: f"{yr}_{i:02d}" for i, c in enumerate(comms) for p in c}
        members.update({f"{yr}_{i:02d}": set(c) for i, c in enumerate(comms)})
        h = dy[dy["home_side"]].assign(team=lambda x: x["pitcher_anon_id"].map(team))
        ht = h.groupby("game_anon_id")["team"].agg(_mode)
        home_team.update(ht.to_dict())
        n_home.update(ht.value_counts().to_dict())

    teams = sorted(t for t, n in n_home.items() if n >= min_home_games)
    years = sorted({int(t[:4]) for t in teams})
    jac = lambda a, b: len(members[a] & members[b]) / len(members[a] | members[b])

    park_of, next_id = {}, 1
    for t in (t for t in teams if t.startswith(str(years[0]))):
        park_of[t], next_id = f"PK{next_id:02d}", next_id + 1
    for y1, y2 in zip(years, years[1:]):
        A = [t for t in teams if t.startswith(str(y1))]
        B = [t for t in teams if t.startswith(str(y2))]
        M = pd.DataFrame([[jac(a, b) for b in B] for a in A], index=A, columns=B)
        for b in B:
            a = M[b].idxmax()
            mutual = M.loc[a].idxmax() == b
            if mutual and M.loc[a, b] >= min_jaccard and a in park_of:
                park_of[b] = park_of[a]
            else:
                park_of[b], next_id = f"PK{next_id:02d}", next_id + 1

    df = df.copy()
    df["home_team_season"] = df["game_anon_id"].map(home_team)
    df["park_id"] = df["home_team_season"].map(park_of)
    return df


def park_summary(df):
    """Una fila por park_id: juegos, densidad mediana del aire y categoría de altitud dominante."""
    g = df.drop_duplicates("game_anon_id").dropna(subset=["park_id"])
    out = g.groupby("park_id").agg(
        games=("game_anon_id", "size"),
        seasons=("year", lambda s: ",".join(map(str, sorted(s.unique())))),
        air_density_median=("air_density_ratio", "median"),
        air_density_se=("air_density_ratio", lambda s: s.std() / np.sqrt(s.notna().sum())),
        altitude_category=("altitude_category", lambda s: s.astype(str).value_counts().index[0]),
        altitude_purity=("altitude_category", lambda s: s.astype(str).value_counts(normalize=True).iat[0]),
    )
    return out.sort_values("air_density_median")


def build_dataset(path=RAW_PATH, save=False):
    """Pipeline completo: limpieza -> secuencias -> run value -> arsenal -> densidad del aire -> parques."""
    df = clean(load_raw(path))
    df = add_sequence_ids(df)
    df, re_table = add_run_value(df)
    df = add_arsenal_features(df)
    df = add_air_density(df)
    df = add_park_ids(df)
    if save:
        PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(PROCESSED_PATH, index=False)
    return df, re_table
