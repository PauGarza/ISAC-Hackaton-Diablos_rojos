"""Gráficas de los reportes para directivos. Lee los resultados del modelo (outputs/resultados y results/)."""
import math, json, os
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

F = os.environ.get('FUENTES_TTF', '')  # carpeta con IBM Plex Sans y Barlow Condensed en .ttf (opcional)
for f in ['IBMPlexSans-Regular.ttf', 'IBMPlexSans-SemiBold.ttf', 'BarlowCondensed-SemiBold.ttf', 'BarlowCondensed-Bold.ttf']:
    if F and os.path.exists(os.path.join(F, f)):
        fm.fontManager.addfont(os.path.join(F, f))
plt.rcParams.update({'font.family': 'IBM Plex Sans', 'font.size': 10.5, 'axes.edgecolor': '#cfc8c9', 'axes.labelcolor': '#4a4345',
                     'xtick.color': '#6c6466', 'ytick.color': '#6c6466', 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.grid': True, 'grid.color': '#ece7e7', 'grid.linewidth': 0.8, 'axes.axisbelow': True,
                     'savefig.dpi': 200, 'savefig.bbox': 'tight', 'savefig.facecolor': 'white'})
MAR, HH, INK, MUT, GRIS = '#0f6aa8', '#b3122e', '#1d1a1b', '#6c6466', '#b9b1b3'
RAIZ = Path(__file__).resolve().parents[2]
R = str(RAIZ / 'outputs' / 'resultados') + '/'
E = str(RAIZ / 'results') + '/'
OUT = str(RAIZ / 'reports' / 'directivos' / 'graficas') + '/'
TIPO = {'Four-Seam': 'Recta', 'Sinker': 'Sinker', 'Cutter': 'Cutter', 'Changeup': 'Cambio', 'Splitter': 'Splitter',
        'Slider': 'Slider', 'Curveball': 'Curva', 'Sweeper': 'Sweeper'}

def titulo(ax, t, sub=None):
    ax.set_title(t, loc='left', fontfamily='Barlow Condensed', fontweight='bold', fontsize=17, color=INK, pad=22 if sub else 10)
    if sub:
        ax.text(0, 1.02, sub, transform=ax.transAxes, fontsize=9.5, color=MUT, va='bottom')

def leyenda(ax, items, loc='lower right'):
    from matplotlib.lines import Line2D
    h = [Line2D([0], [0], marker='o', color='w', markerfacecolor=c, markersize=9, label=l) for l, c in items]
    ax.legend(handles=h, loc=loc, frameon=False, fontsize=9.5)

def guardar(fig, n):
    fig.savefig(OUT + n + '.png'); plt.close(fig)

def dumbbell(filas, n, t, sub, xlab, xlim, ref=100, grupos=None):
    fig, ax = plt.subplots(figsize=(8, 0.42 * len(filas) + 1.4))
    ys = np.arange(len(filas))[::-1]
    for y, (lab, a, b) in zip(ys, filas):
        ax.plot([a, b], [y, y], color='#ddd6d7', lw=4, solid_capstyle='round', zorder=1)
        ax.scatter([a], [y], s=70, color=MAR, zorder=3, edgecolor='white', linewidth=1.5)
        ax.scatter([b], [y], s=70, color=HH, zorder=3, edgecolor='white', linewidth=1.5)
        d = b - a
        ax.text(max(a, b) + (xlim[1] - xlim[0]) * 0.015, y, f'{d:+.0f}'.replace('-', '−'), va='center', fontsize=9.5, color=MUT)
    ax.set_yticks(ys, [f[0] for f in filas]); ax.set_xlim(*xlim); ax.set_xlabel(xlab)
    ax.grid(axis='y', visible=False); ax.tick_params(axis='y', length=0, labelsize=10.5, labelcolor=INK)
    if ref is not None:
        ax.axvline(ref, color=MUT, ls=(0, (3, 3)), lw=1)
    titulo(ax, t, sub)
    from matplotlib.lines import Line2D
    ax.legend(handles=[Line2D([0],[0],marker='o',color='w',markerfacecolor=c,markersize=9,label=l) for l,c in [('Nivel del mar',MAR),('Harp Helú',HH)]], loc='upper center', bbox_to_anchor=(0.5,-0.13), ncol=2, frameon=False, fontsize=9.5)
    guardar(fig, n)

# ---------- Reporte 1 ----------
dt = pd.read_csv(R + 'delta_altitud_por_tipo.csv')
cols = dt.columns.tolist()
def col(df, *cands):
    for c in cands:
        if c in df.columns: return c
    raise KeyError(cands)
ct, cm, ch = col(dt, 'AutoPitchType', 'tipo'), col(dt, 'stuff_mar', 'stuff_plus_mar'), col(dt, 'stuff_hh', 'stuff_plus_hh')
dt = dt[dt[ct].isin(TIPO)].copy(); dt['d'] = dt[ch] - dt[cm]; dt = dt.sort_values('d')
dumbbell([(TIPO[r[ct]], r[cm], r[ch]) for _, r in dt.sort_values('d', ascending=False).iterrows()],
         'r1_stuff_por_tipo', 'El mismo pitcheo vale menos en el Harp Helú', 'Stuff+ medio por tipo, misma mecánica a nivel del mar y a 2,240 m. LMB 2024–2026.',
         'Stuff+ (100 = promedio de la liga)', (82, 116))

es = pd.read_csv(E + 'scores/scores_por_estadio.csv')
fig, ax = plt.subplots(figsize=(8, 4.6))
otros = es[~es.harp_helu]
ax.scatter(otros.altitud_m, otros.stuff_plus, s=55, color=GRIS, edgecolor='white', linewidth=1, zorder=2)
h = es[es.harp_helu].iloc[0]
ax.scatter([h.altitud_m], [h.stuff_plus], s=130, color=HH, edgecolor='white', linewidth=1.5, zorder=3)
ax.annotate('Harp Helú\n2,240 m · 94.4', (h.altitud_m, h.stuff_plus), xytext=(-60, 38), textcoords='offset points', fontsize=10, color=HH,
            fontweight='semibold', arrowprops=dict(arrowstyle='-', color=HH, lw=1))
b = np.polyfit(es.altitud_m, es.stuff_plus, 1)
xx = np.linspace(0, 2300, 50); ax.plot(xx, np.polyval(b, xx), color=MUT, lw=1, ls=(0, (4, 3)))
ax.text(60, 109.5, 'Parques de la costa: 105–108', fontsize=9.5, color=MUT)
ax.text(1300, 90.6, 'Parques de altura: 92–96', fontsize=9.5, color=MUT)
ax.set_xlabel('Altitud del estadio (m)'); ax.set_ylabel('Stuff+ medio de los pitcheos'); ax.set_ylim(89, 111)
titulo(ax, 'Cada 1,000 m de altura le quitan unos 6 puntos al pitcheo', f'Stuff+ medio en los 20 estadios de la LMB. Línea: tendencia ({b[0]*1000:.1f} puntos por cada 1,000 m).')
guardar(fig, 'r1_stuff_por_estadio')

ar = pd.read_csv(R + 'arsenal_combinaciones_harp_helu.csv')
def nom(r):
    rr = 'sin rompiente' if r.rompiente == 'sin rompiente' else TIPO.get(r.rompiente, r.rompiente).lower()
    cc = '' if r.cambio == 'sin cambio' else ' + ' + TIPO.get(r.cambio, r.cambio).lower()
    return f'{TIPO.get(r.recta_principal)} + {rr}{cc}'
ar['nom'] = ar.apply(nom, axis=1); ar = ar.sort_values('stuff_hh')
fig, ax = plt.subplots(figsize=(8, 5.2))
y = np.arange(len(ar))
ax.barh(y, ar.stuff_hh - 80, left=80, color=[HH if v == ar.stuff_hh.max() else '#d98a97' for v in ar.stuff_hh], height=0.62)
ax.scatter(ar.stuff_mar, y, s=46, color=MAR, zorder=3, edgecolor='white', linewidth=1.2)
for yi, (v, n) in enumerate(zip(ar.stuff_hh, ar.pitchers)):
    ax.text(v + 0.6, yi, f'{v:.0f}', va='center', fontsize=9.5, color=INK, fontweight='semibold')
ax.set_yticks(y, [f'{a}  ({n})' for a, n in zip(ar.nom, ar.pitchers)]); ax.tick_params(axis='y', length=0, labelcolor=INK)
ax.set_xlim(80, 122); ax.axvline(100, color=MUT, ls=(0, (3, 3)), lw=1); ax.grid(axis='y', visible=False)
ax.set_xlabel('Stuff+ si toda la liga lanzara en ese entorno')
titulo(ax, 'Cutter + slider: el arsenal que más vale en el Harp Helú', 'Barras: Stuff+ en el Harp Helú. Punto azul: el mismo arsenal a nivel del mar. Entre paréntesis, número de pitchers.')
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
ax.legend(handles=[Patch(color='#d98a97', label='Harp Helú'), Line2D([0], [0], marker='o', color='w', markerfacecolor=MAR, markersize=8, label='Nivel del mar')],
          loc='lower right', frameon=False, fontsize=9.5)
guardar(fig, 'r1_arsenales')

# staff 2026
t = pd.read_csv(R + 'scores_pitcher_temporada.csv'); dp = pd.read_csv(R + 'diablos_pitchers.csv')
r26 = set(t[(t.equipo == 'Diablos') & (t.year == 2026)].pitcher_anon_id)
s26 = dp[dp.pitcher_anon_id.isin(r26)].sort_values('pitching_plus_hh_rel')
fig, ax = plt.subplots(figsize=(8, 0.36 * len(s26) + 1.3))
y = np.arange(len(s26))
c = [HH if v >= 0 else '#d6cfd0' for v in s26.cambio_ranking_pitching_hh]
ax.barh(y, s26.pitching_plus_hh_rel - 60, left=60, color='#e9c3ca', height=0.62)
for yi, (v, d, rol) in enumerate(zip(s26.pitching_plus_hh_rel, s26.cambio_ranking_pitching_hh, s26.rol)):
    ax.text(v + 0.8, yi, f'{v:.0f}', va='center', fontsize=9.5, fontweight='semibold', color=INK)
    dd_=round(d); ax.text(141, yi, ('0' if dd_==0 else f'{dd_:+d}'.replace('-', '−')), va='center', ha='right', fontsize=9.5, color=HH if d >= 3 else (MAR if d <= -3 else MUT), fontweight='semibold' if abs(d) >= 3 else 'normal')
ax.text(141, len(s26) - 0.3, 'en casa', ha='right', fontsize=8.5, color=MUT)
ax.set_yticks(y, [f"{p.replace('pitcher_', '')} · {r[:3]}." for p, r in zip(s26.pitcher_anon_id, s26.rol)]); ax.tick_params(axis='y', length=0, labelcolor=INK)
ax.set_xlim(60, 142); ax.axvline(100, color=MUT, ls=(0, (3, 3)), lw=1); ax.grid(axis='y', visible=False)
ax.set_xlabel('Pitching+ si toda la liga lanzara en el Harp Helú')
titulo(ax, 'Staff 2026 de Diablos ordenado para jugar en casa', 'Pitching+ en ambiente Harp Helú (2024–2026). A la derecha: cuántos puntos sube (+) o baja (−) en el ranking contra nivel del mar.')
guardar(fig, 'r1_staff_2026')

# ---------- Reporte 2 ----------
sp = pd.read_csv(R + 'scores_pitcher.csv'); q = sp[sp.n >= 300].copy()
fig, ax = plt.subplots(figsize=(8, 4.8))
ax.scatter(q.ivb, q.cambio_ranking_pitching_hh, s=16, color=GRIS, alpha=0.75, edgecolor='none')
dq = q[q.pitcher_anon_id.isin(r26)]
ax.scatter(dq.ivb, dq.cambio_ranking_pitching_hh, s=42, color=HH, edgecolor='white', linewidth=1, zorder=3)
bb = np.polyfit(q.ivb, q.cambio_ranking_pitching_hh, 1); xx = np.linspace(q.ivb.min(), q.ivb.max(), 20)
ax.plot(xx, np.polyval(bb, xx), color=INK, lw=1.2)
r = q.ivb.corr(q.cambio_ranking_pitching_hh)
ax.axhline(0, color=MUT, lw=1)
ax.set_xlabel('Bote vertical inducido promedio del arsenal (in)'); ax.set_ylabel('Puntos que gana en el Harp Helú')
ax.text(0.98, 0.95, f'r = {r:.2f}'.replace('-', '−'), transform=ax.transAxes, ha='right', fontsize=11, color=INK, fontweight='semibold')
titulo(ax, 'Entre menos depende del bote, más gana en casa', '601 pitchers con al menos 300 pitcheos. Rojo: staff de Diablos 2026.')
leyenda(ax, [('Pitchers de la liga', GRIS), ('Diablos 2026', HH)], loc='lower left')
guardar(fig, 'r2_bote_vs_ganancia')

rasgos = [('Bote vertical (IVB)', q.ivb.corr(q.cambio_ranking_pitching_hh)), ('Corrida lateral (|HB|)', q.hb.abs().corr(q.cambio_ranking_pitching_hh)),
          ('% de rodados', q.gb_bip.corr(q.cambio_ranking_pitching_hh)), ('Spin', q.spin.corr(q.cambio_ranking_pitching_hh)),
          ('Velocidad', q.velo.corr(q.cambio_ranking_pitching_hh))]
rasgos.sort(key=lambda x: x[1])
fig, ax = plt.subplots(figsize=(8, 3.3))
y = np.arange(len(rasgos))
ax.barh(y, [v for _, v in rasgos], color=[HH if v > 0.1 else (MAR if v < -0.1 else GRIS) for _, v in rasgos], height=0.6)
for yi, (_, v) in enumerate(rasgos):
    ax.text(v + (0.02 if v >= 0 else -0.02), yi, f'{v:+.2f}'.replace('-', '−'), va='center', ha='left' if v >= 0 else 'right', fontsize=9.5, color=INK)
ax.set_yticks(y, [n for n, _ in rasgos]); ax.tick_params(axis='y', length=0, labelcolor=INK); ax.axvline(0, color=MUT, lw=1)
ax.set_xlim(-0.8, 0.6); ax.grid(axis='y', visible=False); ax.set_xlabel('Correlación con los puntos que gana en el Harp Helú')
titulo(ax, 'Qué rasgos ayudan y cuáles estorban en la altura', 'Rojo: ayuda a subir en el ranking del Harp Helú. Azul: hace bajar. Gris: no distingue.')
guardar(fig, 'r2_rasgos')

fo = pd.read_csv(R + 'delta_altitud_por_forma.csv')
fig, ax = plt.subplots(figsize=(8.4, 6))
OFF = {11: (-0.5, 0.7, 'right'), 12: (-0.6, 0.2, 'right'), 13: (0.5, 0.7, 'left'), 7: (0.5, -1.2, 'left'), 9: (0.5, 0.6, 'left')}
norm = plt.Normalize(-26, -6); cmap = LinearSegmentedColormap.from_list('d', [HH, '#e6a9b3', '#c9c3c4'])
for _, r_ in fo.iterrows():
    cc = cmap(norm(r_.delta_stuff))
    ax.annotate('', xy=(r_.hb_hh, r_.ivb_hh), xytext=(r_.hb_mar, r_.ivb_mar), arrowprops=dict(arrowstyle='-|>', color=cc, lw=1.6, mutation_scale=11))
    ax.scatter([r_.hb_mar], [r_.ivb_mar], s=30 + r_.n / 1500, color=cc, edgecolor='white', linewidth=1, zorder=3)
    dx, dy, ha = OFF.get(_, (0.5, 0.6, 'left'))
    ax.text(r_.hb_mar + dx, r_.ivb_mar + dy, f'{r_.forma_nombre.split(" ")[0].replace("Four-Seam","Recta").replace("Curveball","Curva").replace("Changeup","Cambio")} {r_.delta_stuff:+.0f}'.replace('-', '−'), fontsize=8.5, color=INK, ha=ha)
ax.axhline(0, color=MUT, lw=0.8); ax.axvline(0, color=MUT, lw=0.8)
ax.set_xlabel('Movimiento horizontal (in)   ← guante · brazo →'); ax.set_ylabel('Bote vertical inducido (in)')
titulo(ax, 'Mapa de movimiento: todo se encoge hacia el centro', '14 formas de pitcheo de la LMB. Punto: nivel del mar; flecha: a dónde llega en el Harp Helú. Número: cambio de Stuff+.')
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm); ax.set_xlim(-15, 21); cb = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.03); cb.set_label('Cambio de Stuff+ en el Harp Helú'); cb.outline.set_visible(False)
guardar(fig, 'r2_mapa_movimiento')

# ---------- Reporte 3 ----------
fo2 = fo.sort_values('delta_stuff', ascending=True)
def corto(s):
    s = s.replace('Four-Seam', 'Recta').replace('Curveball', 'Curva').replace('Changeup', 'Cambio')
    return s
fig, ax = plt.subplots(figsize=(8, 5.6))
y = np.arange(len(fo2))
ax.barh(y, fo2.delta_stuff, color=[cmap(norm(v)) for v in fo2.delta_stuff], height=0.62)
for yi, v in enumerate(fo2.delta_stuff):
    ax.text(v - 0.3, yi, f'{v:.0f}'.replace('-', '−'), va='center', ha='right', fontsize=9.5, color=INK)
ax.set_yticks(y, [corto(s) for s in fo2.forma_nombre], fontsize=9); ax.tick_params(axis='y', length=0, labelcolor=INK, labelright=True, labelleft=False)
ax.set_xlim(-28, 0); ax.grid(axis='y', visible=False); ax.set_xlabel('Puntos de Stuff+ que pierde en el Harp Helú')
titulo(ax, 'Qué formas aguantan la altura y cuáles no', 'Todas pierden; la diferencia está en cuánto. Arriba: las que más aguantan.')
guardar(fig, 'r3_formas')

rk = pd.read_csv(R + 'riesgo_contacto_duro_hr.csv')
rk['t'] = rk.tipo.map(TIPO)
hh_ = rk[rk.entorno == 'Harp Helú'].set_index('t'); mr_ = rk[rk.entorno != 'Harp Helú'].set_index('t')
orden = (hh_.hr_por_100_pitcheos - mr_.hr_por_100_pitcheos).sort_values().index.tolist()
fig, axs = plt.subplots(1, 2, figsize=(9, 4.2), sharey=True)
for ax, c_, lab, lim in [(axs[0], 'pct_contacto_duro', 'Contacto duro (% de bolas en juego ≥ 95 mph)', (12, 32)), (axs[1], 'hr_por_100_pitcheos', 'Jonrones por cada 100 pitcheos', (0.3, 1.3))]:
    for yi, tt in enumerate(orden):
        a, b_ = mr_.loc[tt, c_], hh_.loc[tt, c_]
        ax.plot([a, b_], [yi, yi], color='#ddd6d7', lw=4, solid_capstyle='round')
        ax.scatter([a], [yi], s=60, color=MAR, zorder=3, edgecolor='white'); ax.scatter([b_], [yi], s=60, color=HH, zorder=3, edgecolor='white')
    ax.set_xlim(*lim); ax.set_xlabel(lab, fontsize=9.5); ax.grid(axis='y', visible=False)
axs[0].set_yticks(range(len(orden)), orden); axs[0].tick_params(axis='y', length=0, labelcolor=INK)
titulo(axs[0], 'El riesgo extra de contacto duro y jonrón', 'Harp Helú contra parques a menos de 700 m. Ordenado de menor a mayor aumento de jonrones.')
leyenda(axs[1], [('Nivel del mar', MAR), ('Harp Helú', HH)])
guardar(fig, 'r3_riesgo_hr')

mp = pd.read_csv(R + 'mapa_ubicacion_por_grupo.csv')
filas_ = ['alto fuera', 'alto', 'medio', 'bajo', 'bajo fuera']; cols_ = ['brazo fuera', 'brazo', 'centro', 'guante', 'guante fuera']
fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.9))
cm2 = LinearSegmentedColormap.from_list('r', [HH, '#f3d2d8', '#ffffff', '#d4e6f3'])
nrm = TwoSlopeNorm(vmin=-8, vcenter=0, vmax=2)
for ax, g, nombre in zip(axs, ['FB', 'BRK', 'OFF'], ['Rectas y sinkers', 'Rompientes', 'Cambios y splitters']):
    m = np.full((5, 5), np.nan)
    for _, r_ in mp[mp.grupo == g].iterrows():
        m[filas_.index(r_.alto), cols_.index(r_.lado)] = r_.delta_hh
    ax.imshow(m, cmap=cm2, norm=nrm)
    for i in range(5):
        for j in range(5):
            ax.text(j, i, f'{m[i, j]:.0f}'.replace('-', '−') if abs(m[i, j]) >= 0.5 else '0', ha='center', va='center', fontsize=9, color=INK)
    ax.add_patch(plt.Rectangle((0.5, 0.5), 3, 3, fill=False, lw=2, color=INK))
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title(nombre, fontsize=11, color=INK, fontweight='semibold')
    ax.set_xlabel('brazo  ←  →  guante', fontsize=8.5, color=MUT)
fig.suptitle('Dónde castiga la altura: el centro de la zona', x=0.02, ha='left', fontfamily='Barlow Condensed', fontweight='bold', fontsize=17, color=INK, y=1.12)
fig.text(0.02, 1.03, 'Cambio de Pitching+ en el Harp Helú por ubicación, vista desde el catcher, lado del brazo y del guante del pitcher. Recuadro: zona de strike.', fontsize=9.5, color=MUT)
guardar(fig, 'r3_zona')

mz = pd.read_csv(R + 'diablos_mezcla_casa_vs_visita.csv').fillna(0)
mz['t'] = mz.AutoPitchType.map(TIPO); mz = mz.sort_values('Harp Helú')
fig, ax = plt.subplots(figsize=(8, 4))
y = np.arange(len(mz))
ax.barh(y + 0.19, mz['visita'], height=0.36, color='#9cc3df', label='De visita')
ax.barh(y - 0.19, mz['Harp Helú'], height=0.36, color=HH, label='En casa (Harp Helú)')
for yi, (a, b_) in enumerate(zip(mz['Harp Helú'], mz['visita'])):
    ax.text(a + 0.4, yi - 0.19, f'{a:.0f} %', va='center', fontsize=9, color=INK); ax.text(b_ + 0.4, yi + 0.19, f'{b_:.0f} %', va='center', fontsize=9, color=MUT)
ax.set_yticks(y, mz.t); ax.tick_params(axis='y', length=0, labelcolor=INK); ax.grid(axis='y', visible=False); ax.set_xlim(0, 38)
ax.set_xlabel('% de los pitcheos de Diablos'); ax.legend(frameon=False, loc='lower right')
titulo(ax, 'En casa, Diablos lanza más rectas y menos sliders', 'Mezcla de pitcheos del staff, Harp Helú contra visita, 2024–2026. La altura pide lo contrario.')
guardar(fig, 'r3_mezcla')

mc = pd.read_csv(E + 'bayes_mcmc/castigo_altitud_pitcher_tipo_mcmc.csv')
mc = mc[mc.AutoPitchType.isin(['Four-Seam', 'Sinker', 'Cutter', 'Changeup', 'Slider', 'Curveball'])]
g = mc.groupby('AutoPitchType').agg(m=('castigo_post', 'mean'), lo=('castigo_post', lambda s: s.quantile(0.1)), hi=('castigo_post', lambda s: s.quantile(0.9))).sort_values('m')
fig, ax = plt.subplots(figsize=(8, 3.4))
y = np.arange(len(g))
ax.hlines(y, g.lo, g.hi, color='#e6a9b3', lw=6)
ax.scatter(g.m, y, s=70, color=HH, zorder=3, edgecolor='white', linewidth=1.5)
for yi, v in enumerate(g.m): ax.text(g.hi.iloc[yi] + 0.08, yi, f'{v:.1f}', va='center', fontsize=9.5, color=INK)
ax.set_yticks(y, [TIPO[i] for i in g.index]); ax.tick_params(axis='y', length=0, labelcolor=INK); ax.grid(axis='y', visible=False)
ax.set_xlabel('Carreras extra por cada 100 pitcheos en altura (modelo bayesiano)')
titulo(ax, 'Castigo esperado en altura por tipo de pitcheo', 'Punto: castigo promedio. Barra: rango del 80 % central de los pitchers de la liga.')
guardar(fig, 'r3_castigo_bayes')

# ---------- Reporte 5 ----------
v = [('Pitchers nuevos\n(Stuff+)', 0.44), ('Temporada 2026\n(Stuff+)', 0.42), ('Temporada 2026\n(Pitching+)', 0.56), ('Harp Helú apartado\n(Stuff+)', 0.66), ('Harp Helú apartado\n(Pitching+)', 0.62)]
base = [-0.37, -0.26, -0.26, -0.20, -0.20]
fig, ax = plt.subplots(figsize=(8, 3.8))
x = np.arange(len(v))
ax.bar(x - 0.19, [b for _, b in v], width=0.36, color=HH, label='Nuestro modelo')
ax.bar(x + 0.19, base, width=0.36, color=GRIS, label='Referencia del reto (promedio por cuenta)')
for xi, (_, b_) in enumerate(v): ax.text(xi - 0.19, b_ + 0.02, f'{b_:.2f}', ha='center', fontsize=9.5, color=INK, fontweight='semibold')
for xi, b_ in enumerate(base): ax.text(xi + 0.19, b_ - 0.06, f'{b_:.2f}'.replace('-', '−'), ha='center', fontsize=9, color=MUT)
ax.axhline(0, color=MUT, lw=1); ax.set_xticks(x, [n for n, _ in v], fontsize=9); ax.set_ylim(-0.5, 0.95); ax.grid(axis='x', visible=False)
ax.set_ylabel('Correlación con las carreras reales\npor pitcher'); ax.legend(frameon=False, loc='upper left', fontsize=9, ncol=2)
titulo(ax, 'El modelo acierta con datos que no vio', 'Correlación entre la calidad estimada y las carreras que realmente permitió cada pitcher, en datos fuera del entrenamiento.')
guardar(fig, 'r5_validacion')

fig, ax = plt.subplots(figsize=(8, 3.2))
pares = [('Stuff+ → su Stuff+ del año siguiente', 0.61, 0.68), ('Pitching+ → sus carreras del año siguiente', 0.31, 0.38), ('Carreras → sus carreras del año siguiente', 0.23, 0.29)]
y = np.arange(len(pares))[::-1]
for yi, (n_, a, b_) in zip(y, pares):
    col_ = HH if n_.startswith('Stuff+') else (MAR if 'Pitching' in n_ else GRIS)
    ax.hlines(yi, a, b_, color=col_, lw=7, alpha=0.85)
    ax.text(b_ + 0.015, yi, f'{a:.2f}–{b_:.2f}', va='center', fontsize=9.5, color=INK)
ax.set_yticks(y, [p[0] for p in pares]); ax.tick_params(axis='y', length=0, labelcolor=INK); ax.set_xlim(0, 0.8); ax.grid(axis='y', visible=False)
ax.set_xlabel('Correlación entre un año y el siguiente (2024→25 y 2025→26)')
titulo(ax, 'El Stuff+ se repite y anticipa las carreras', 'Pitching+ predice las carreras del año siguiente mejor que las propias carreras del año anterior.')
guardar(fig, 'r5_estabilidad')
print('ok')
