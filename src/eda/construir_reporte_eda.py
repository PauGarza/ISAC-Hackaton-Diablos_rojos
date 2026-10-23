"""Construye reporte_eda.html (autocontenido, gráficas SVG) a partir de los CSV de eda_modelo."""
import io, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[2]
E = str(RAIZ / "results" / "eda") + "/"
G = str(RAIZ / "reports" / "eda") + "/"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#888", "axes.labelcolor": "#333", "xtick.color": "#555", "ytick.color": "#555"})
AZ, RO, GR = "#2a6fdb", "#c8102e", "#9aa4b2"

import os
os.makedirs(G + "graficas", exist_ok=True)
_n = iter(["01_volumen", "02_mezcla", "03_correlaciones", "04_movimiento_por_tipo", "05_ivb_recta", "06_distancia_elevado", "07_contacto_duro", "08_hr_por_bip"])
def svg(fig):
    fig.savefig(G + f"graficas/{next(_n)}.png", dpi=150, bbox_inches="tight")
    b = io.StringIO(); fig.savefig(b, format="svg", bbox_inches="tight"); plt.close(fig)
    s = b.getvalue(); return s[s.index("<svg"):]

est = pd.read_csv(E + "efecto_altitud_por_estadio.csv")
cor = pd.read_csv(E + "correlacion_con_altitud.csv", index_col=0).r_con_altitud
vol = pd.read_csv(E + "volumen_temporada_altitud.csv", index_col=0)
mez = pd.read_csv(E + "mezcla_pitcheos.csv", index_col=0).pitcheos
mov = pd.read_csv(E + "movimiento_por_tipo_alto_vs_bajo.csv", index_col=0)
cal = pd.read_csv(E + "calidad_datos.csv", index_col=0).valor
hh = est.estadio.str.contains("Harp")

def scatter(col, ylab, titulo):
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.scatter(est.altitud_m[~hh], est[col][~hh], s=28, color=AZ, alpha=.85)
    ax.scatter(est.altitud_m[hh], est[col][hh], s=60, color=RO, zorder=3)
    m, b = np.polyfit(est.altitud_m, est[col], 1); x = np.array([0, 2300])
    ax.plot(x, m * x + b, color=GR, lw=1.2, ls="--")
    r = est[est.estadio.str.contains("Harp")].iloc[0]
    ax.annotate("Harp Helú", (r.altitud_m, r[col]), xytext=(-62, 14 if m < 0 else 8), textcoords="offset points", color=RO, fontsize=9)
    ax.set_xlabel("Altitud del estadio (m)"); ax.set_ylabel(ylab)
    ax.set_title(f"{titulo}  (r = {cor.get(col, np.corrcoef(est.altitud_m, est[col])[0,1]):.2f})", loc="left", fontsize=10.5)
    ax.grid(axis="y", color="#eee"); return svg(fig)

# Volumen
fig, ax = plt.subplots(figsize=(6.4, 2.8))
v = vol.drop(index="All").drop(columns="All")[["Extreme Altitude", "Medium Altitude", "No Altitude"]]
izq = np.zeros(len(v)); cols = [RO, "#e8a33d", AZ]; et = ["Altitud extrema", "Altitud media", "Nivel del mar"]
for c, cc, e in zip(v.columns, cols, et):
    ax.barh(v.index.astype(str), v[c], left=izq, color=cc, label=e); izq += v[c].values
ax.invert_yaxis(); ax.set_xlabel("Pitcheos"); ax.legend(frameon=False, ncol=3, loc="lower center", bbox_to_anchor=(.5, 1.0))
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}k")); g_vol = svg(fig)

# Mezcla
m7 = mez.head(7); nombres = {"Four-Seam": "Recta", "Slider": "Slider", "Sinker": "Sinker", "Changeup": "Changeup",
                             "Curveball": "Curva", "Cutter": "Cutter", "Splitter": "Splitter"}
fig, ax = plt.subplots(figsize=(6.4, 2.8)); pct = 100 * m7 / mez.sum()
ax.barh([nombres[i] for i in m7.index], pct, color=AZ); ax.invert_yaxis()
for i, p in enumerate(pct): ax.text(p + .4, i, f"{p:.1f} %", va="center", fontsize=9)
ax.set_xlabel("% de pitcheos"); g_mez = svg(fig)

# Correlaciones
lab = {"ivb_recta": "Bote inducido de la recta", "hb_recta": "Corrida de la recta", "velo_recta": "Velocidad de la recta",
       "spin_recta": "Giro de la recta", "whiff_por_swing_%": "Whiff por swing", "contacto_duro_pct": "Contacto duro (≥95 mph)",
       "distancia_elevado_pies": "Distancia del elevado", "hr_por_bip_%": "HR por bola en juego"}
c = cor.sort_values()
fig, ax = plt.subplots(figsize=(6.4, 3.2))
ax.barh([lab[i] for i in c.index], c, color=[RO if x < 0 else AZ for x in c]); ax.axvline(0, color="#888", lw=.8)
for i, x in enumerate(c): ax.text(x + (.03 if x >= 0 else -.03), i, f"{x:.2f}", va="center", ha="left" if x >= 0 else "right", fontsize=9)
ax.set_xlim(-1.2, 1.2); ax.set_xlabel("Correlación con la altitud (20 estadios)"); g_cor = svg(fig)

# Movimiento por tipo
orden = ["Four-Seam", "Sinker", "Cutter", "Changeup", "Slider", "Curveball"]
fig, axs = plt.subplots(1, 2, figsize=(6.8, 2.9), sharey=True)
y = np.arange(len(orden))
for ax, var, tit in zip(axs, ["ivb", "hb"], ["Bote inducido (|in|)", "Corrida (|in|)"]):
    ax.barh(y - .2, mov.loc[orden, f"{var}_bajo"].abs(), .4, color=AZ, label="< 700 m")
    ax.barh(y + .2, mov.loc[orden, f"{var}_alto"].abs(), .4, color=RO, label="≥ 1,800 m")
    ax.set_title(tit, loc="left", fontsize=10); ax.set_yticks(y, [nombres[o] for o in orden])
axs[0].invert_yaxis(); axs[0].legend(frameon=False, fontsize=8.5, loc="lower right"); g_mov = svg(fig)

g_ivb = scatter("ivb_recta", "Bote inducido (in)", "Bote inducido de la recta")
g_dis = scatter("distancia_elevado_pies", "Distancia (pies)", "Distancia media del elevado")
g_dur = scatter("contacto_duro_pct", "% de bolas en juego", "Contacto duro")
g_hr = scatter("hr_por_bip_%", "% de bolas en juego", "Jonrones por bola en juego")

t_est = est[["estadio", "altitud_m", "pitcheos", "ivb_recta", "hb_recta", "velo_recta", "spin_recta", "contacto_duro_pct",
             "distancia_elevado_pies", "hr_por_bip_%", "whiff_por_swing_%"]].copy()
filas = "".join(
    f"<tr{' class=hh' if 'Harp' in r.estadio else ''}><td>{r.estadio}</td><td>{r.altitud_m:,.0f}</td><td>{r.pitcheos:,}</td>"
    f"<td>{r.ivb_recta:.1f}</td><td>{r.hb_recta:.1f}</td><td>{r.velo_recta:.1f}</td><td>{r.spin_recta:,.0f}</td>"
    f"<td>{r.contacto_duro_pct:.1f}</td><td>{r.distancia_elevado_pies:.0f}</td><td>{r['hr_por_bip_%']:.1f}</td><td>{r['whiff_por_swing_%']:.1f}</td></tr>"
    for r in t_est.itertuples(index=False) for r in [pd.Series(r._asdict()).rename({"_9": "hr_por_bip_%", "_10": "whiff_por_swing_%"})])
filas_mov = "".join(
    f"<tr><td>{nombres[o]}</td><td>{mov.loc[o,'ivb_alto']:.1f} / {mov.loc[o,'ivb_bajo']:.1f}</td><td>{mov.loc[o,'hb_alto']:.1f} / {mov.loc[o,'hb_bajo']:.1f}</td>"
    f"<td>{mov.loc[o,'velo_alto']:.1f} / {mov.loc[o,'velo_bajo']:.1f}</td><td>{mov.loc[o,'spin_alto']:,.0f} / {mov.loc[o,'spin_bajo']:,.0f}</td></tr>" for o in orden)

html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>EDA Stuff+ LMB</title><style>
:root{{--tx:#1d2330;--mu:#5b6473;--bd:#e3e6eb;--ac:#c8102e;--bg:#fff}}
body{{margin:0;background:var(--bg);color:var(--tx);font:15px/1.55 -apple-system,"Segoe UI",Helvetica,Arial,sans-serif}}
main{{max-width:820px;margin:0 auto;padding:32px 16px 48px}}
h1{{font-size:26px;margin:0 0 4px}} h2{{font-size:19px;margin:34px 0 8px;border-bottom:2px solid var(--ac);padding-bottom:4px}}
.sub{{color:var(--mu);margin:0 0 20px}} figure{{margin:14px 0 6px}} figure svg{{width:100%;height:auto}}
figcaption{{color:var(--mu);font-size:13px}} .kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin:16px 0}}
.k{{border:1px solid var(--bd);border-radius:8px;padding:10px 12px}} .k b{{display:block;font-size:21px}} .k span{{color:var(--mu);font-size:12.5px}}
.tw{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;font-size:12.5px;margin:10px 0}}
th,td{{border-bottom:1px solid var(--bd);padding:5px 6px;text-align:right}} th:first-child,td:first-child{{text-align:left}}
th{{background:#f5f6f8;font-weight:600}} tr.hh td{{color:var(--ac);font-weight:600}}
table.txt td,table.txt th{{text-align:left}} h3{{break-after:avoid}}
ul{{padding-left:20px}} li{{margin:4px 0}} .nota{{color:var(--mu);font-size:13px}}
@media print{{main{{padding:0}} h2{{break-after:avoid}} figure,table{{break-inside:avoid}}}}
</style></head><body><main>
<h1>EDA: datos LMB y efecto de la altitud</h1>
<p class="sub">Hackathon Diablos Rojos · Stuff+ calibrado al Estadio Alfredo Harp Helú (2,240 m) · 18 de octubre de 2026</p>

<h2>En una página</h2>
<ul>
<li>Antes de cualquier modelo, los datos ya muestran el efecto de la altitud: entre más alto el estadio, <b>menos se mueve la recta</b> (r = {cor.ivb_recta:.2f}) y <b>más lejos vuela el elevado</b> (r = {cor.distancia_elevado_pies:.2f}).</li>
<li>La recta pasa de ~17.5 pulgadas de bote inducido en la costa a 12.2 en el Harp Helú; el elevado promedio, de ~289 a 324 pies.</li>
<li>La velocidad y el giro casi no cambian con la altitud (r = {cor.velo_recta:.2f} y {cor.spin_recta:.2f}). La pelota sale igual; lo que cambia es cuánto la empuja el aire (efecto Magnus).</li>
<li>El contacto duro sube con la altitud (r = {cor.contacto_duro_pct:.2f}), pero los jonrones por bola en juego casi no (r = {cor['hr_por_bip_%']:.2f}).</li>
<li>Estas observaciones definen el modelo: altitud continua en metros, forma completa del pitcheo en vez de solo giro, y una cabeza aparte para el valor del contacto.</li>
</ul>

<h2>1. Los datos</h2>
<div class="kpis">
<div class="k"><b>{cal.pitcheos:,}</b><span>pitcheos Trackman</span></div>
<div class="k"><b>{cal.juegos:,}</b><span>juegos</span></div>
<div class="k"><b>{cal.pitchers:,}</b><span>pitchers</span></div>
<div class="k"><b>{cal.bateadores:,}</b><span>bateadores</span></div>
<div class="k"><b>20</b><span>estadios</span></div>
</div>
<p>Tres temporadas de la LMB (2024, 2025 y 2026 parcial). Cerca de la mitad de los pitcheos se lanzó en parques con altitud, lo que permite comparar al mismo pitcher en distintos entornos.</p>
<figure>{g_vol}<figcaption>Pitcheos por temporada y categoría de altitud. Fuente: volumen_temporada_altitud.csv.</figcaption></figure>

<h2>2. Mezcla de pitcheos</h2>
<figure>{g_mez}<figcaption>Participación por tipo (AutoPitchType). Fuente: mezcla_pitcheos.csv.</figcaption></figure>
<p>El clasificador casi no usa «Sweeper» (0.1 %), así que los sweepers quedan dentro de «Slider». Por eso el modelo mira la forma del pitcheo y no la etiqueta.</p>

<h2>3. Calidad de datos</h2>
<ul>
<li>No hay ID de estadio, solo la categoría de altitud. El estadio de cada juego se infirió por equipo local (récords 2024-2025 y altitud de la ciudad); el Harp Helú es la casa del equipo con mejor récord. Es una inferencia, no un dato confirmado por ISAC.</li>
<li>No hay corredores en base, fecha, umpire ni clima. Por eso el valor en carreras se calcula por cuenta (balls-strikes) y no con RE24.</li>
<li><code>is_hit_by_pitch</code> viene siempre en 0 aunque hay golpeados; se recalcula desde PitchCall.</li>
<li>{cal.plateloc_height_0:,} pitcheos con PlateLocHeight = 0 exacto (se tratan como faltantes), {cal.sin_pitcher_id:,} sin ID de pitcher y {cal.sin_estadio:,} sin estadio asignado.</li>
<li><code>EffectiveVelo</code> llega como texto y se convierte a número.</li>
</ul>

<h2>4. La altitud en crudo, por estadio</h2>
<figure>{g_ivb}<figcaption>Bote inducido medio de las rectas en cada estadio, 2024-2026. Rojo: Harp Helú. Línea punteada: ajuste lineal.</figcaption></figure>
<figure>{g_dis}<figcaption>Distancia media de los elevados (FlyBall) por estadio.</figcaption></figure>
<figure>{g_dur}<figcaption>Contacto duro: % de bolas en juego con velocidad de salida ≥ 95 mph.</figcaption></figure>
<figure>{g_hr}<figcaption>Jonrones por bola en juego. La relación es débil: el exceso de ofensiva en altura viene más de hits que de jonrones (en línea con Richardson, 2014).</figcaption></figure>
<figure>{g_cor}<figcaption>Correlación de cada métrica con la altitud entre los 20 estadios. Fuente: correlacion_con_altitud.csv.</figcaption></figure>

<div class="tw" style="break-before:page"><h3>Tabla por estadio</h3><table><thead><tr><th>Estadio</th><th>Altitud (m)</th><th>Pitcheos</th><th>IVB recta (in)</th><th>HB recta (in)</th><th>Velo recta (mph)</th><th>Giro recta (rpm)</th><th>Contacto duro %</th><th>Dist. elevado (ft)</th><th>HR/BIP %</th><th>Whiff/swing %</th></tr></thead><tbody>{filas}</tbody></table></div>
<p class="nota">Fuente: efecto_altitud_por_estadio.csv. Corrida (HB) con zurdos espejados.</p>

<h2>5. Por tipo de pitcheo</h2>
<p>En parques de 1,800 m o más todos los pitcheos se mueven menos que en parques de menos de 700 m, mientras la velocidad y el giro no cambian. Son promedios crudos que mezclan pitchers distintos; el modelo compara al mismo pitcher.</p>
<figure>{g_mov}<figcaption>Movimiento absoluto por tipo, parques altos contra bajos. Fuente: movimiento_por_tipo_alto_vs_bajo.csv.</figcaption></figure>
<div class="tw"><table><thead><tr><th>Pitcheo</th><th>IVB alto / bajo (in)</th><th>HB alto / bajo (in)</th><th>Velo alto / bajo (mph)</th><th>Giro alto / bajo (rpm)</th></tr></thead><tbody>{filas_mov}</tbody></table></div>
<p>La recta pierde 4 pulgadas de bote; el sinker y el changeup, 4 de corrida. El slider pierde poco en pulgadas porque se mueve poco desde el inicio.</p>

<h2>6. Qué decisiones del modelo salen del EDA</h2>
<div class="tw"><table class="txt"><thead><tr><th>Lo que muestra el EDA</th><th>Decisión de modelado</th></tr></thead><tbody>
<tr><td>El movimiento cae de forma continua con la altitud (r = {cor.ivb_recta:.2f} en la recta), no solo en el Harp Helú</td><td>La altitud entra como variable continua en metros</td></tr>
<tr><td>Velocidad y giro no cambian; el movimiento sí</td><td>Se modela la forma completa (movimiento, eje, separación con la recta) y no solo el giro (H4)</td></tr>
<tr><td>El elevado viaja ~35 pies más arriba de 1,800 m</td><td>Una cabeza aparte para el valor del contacto según velocidad, ángulo y altitud (H3)</td></tr>
<tr><td>Los pitchers lanzan en varios entornos</td><td>Comparaciones dentro del mismo pitcher y un modelo bayesiano jerárquico (MCMC) que usa su historia en altura</td></tr>
<tr><td>El clasificador mete sweepers en «Slider»</td><td>Stuff+ no recibe la etiqueta del tipo, solo la forma</td></tr>
<tr><td>No hay corredores ni estadio</td><td>Valor en carreras por cuenta; estadio inferido por equipo local</td></tr>
</tbody></table></div>
<p class="nota">Código: eda_altitud.py. Todos los CSV están en la misma carpeta eda_modelo.</p>
</main></body></html>"""
open(G + "reporte_eda.html", "w", encoding="utf-8").write(html)
print(len(html))
