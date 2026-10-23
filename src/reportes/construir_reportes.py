"""Construye los reportes para directivos: MD -> HTML con estilo -> PDF.

Uso: python3 construir_reportes.py
Necesita pandoc, Playwright (Chromium) y pypdf. Las fuentes woff2 van en fuentes/.
"""
import base64, html, os, re, subprocess, sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2] / "reports" / "directivos"
MD, OUT, FUENTES = BASE / "md", BASE / "html", BASE / "fuentes"
PDF = BASE / "pdf"
# Chromium: variable de entorno CHROME, o el primero que exista (Linux del proyecto, Chrome/Edge en Windows)
CHROME = os.environ.get("CHROME") or next(
    (c for c in ["/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
                 r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                 r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"] if Path(c).exists()), None)
FECHA = "Octubre 2026"
EQUIPO = os.environ.get("EQUIPO", "Paulina Garza Allende, Othoniel Reyes Camacho, Andrea Guerra y Jose Rodrigo Dumas Avalos")


def b64(p):
    return base64.b64encode(Path(p).read_bytes()).decode()


def fuentes_css():
    defs = [("Plex", 400, "IBMPlexSans-Regular"), ("Plex", 600, "IBMPlexSans-SemiBold"),
            ("Barlow", 600, "BarlowCondensed-SemiBold"), ("Barlow", 700, "BarlowCondensed-Bold")]
    return "\n".join(
        f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:normal;font-display:swap;'
        f'src:url(data:font/woff2;base64,{b64(FUENTES / (f + ".woff2"))}) format("woff2")}}'
        for fam, w, f in defs)


CSS = r"""
:root{--bg:#f6f4f1;--papel:#fff;--tinta:#1d1a1b;--mut:#6c6466;--linea:#e4dede;--suave:#f3efee;
--rojo:#b3122e;--rojo-suave:#fbecef;--azul:#0f6aa8;--ambar:#9a6700;--ambar-suave:#fff6e0;
--disp:"Barlow","Arial Narrow",sans-serif;--cuerpo:"Plex",system-ui,sans-serif;color-scheme:light}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--tinta);font:16px/1.6 var(--cuerpo);font-variant-numeric:tabular-nums}
.hoja{max-width:860px;margin:0 auto;background:var(--papel);min-height:100vh;box-shadow:0 0 0 1px var(--linea)}
.portada{background:var(--tinta);color:#fff;padding:28px 40px 30px;position:relative;overflow:hidden}
.portada:after{content:"";position:absolute;left:0;right:0;bottom:0;height:6px;background:var(--rojo)}
.ceja{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font:600 13px/1.3 var(--cuerpo);letter-spacing:.12em;text-transform:uppercase;color:#d9cfd1}
.ceja b{color:#fff}
.titular{display:flex;gap:22px;align-items:flex-end;margin-top:22px}
.num{font:700 108px/.8 var(--disp);color:var(--rojo);letter-spacing:-.02em}
h1{font:700 46px/1.02 var(--disp);margin:0;letter-spacing:.005em}
.pregunta{margin:16px 0 0;font-size:17px;line-height:1.5;color:#e9e1e2;max-width:680px}
.meta{margin-top:18px;font-size:13px;color:#b9adb0}
.cuerpo{padding:30px 40px 48px}
h2{font:700 30px/1.1 var(--disp);margin:44px 0 12px;padding-top:12px;border-top:2px solid var(--tinta)}
h3{font:600 22px/1.2 var(--disp);margin:28px 0 8px}
p{margin:0 0 14px}
ul,ol{margin:0 0 16px;padding-left:22px}
li{margin-bottom:7px}
strong{font-weight:600}
a{color:var(--rojo);overflow-wrap:anywhere}
code{font:13px/1.4 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--suave);padding:1px 5px;border-radius:4px;overflow-wrap:anywhere}
blockquote{margin:20px 0;padding:14px 18px;background:var(--rojo-suave);border-left:5px solid var(--rojo);border-radius:0 8px 8px 0}
blockquote p:last-child,blockquote ul:last-child{margin-bottom:0}
blockquote.resumen{background:var(--suave);border-left-color:var(--tinta);padding:18px 22px;margin-top:0}
blockquote.resumen>p:first-child{font:700 15px/1 var(--cuerpo);text-transform:uppercase;letter-spacing:.12em;color:var(--rojo);margin-bottom:12px}
blockquote.resumen li{margin-bottom:9px}
blockquote.aviso{background:var(--ambar-suave);border-left-color:var(--ambar)}
figure{margin:22px 0 24px;break-inside:avoid}
figure img{display:block;width:100%;height:auto;border:1px solid var(--linea);border-radius:8px;background:#fff}
figcaption{font-size:13px;color:var(--mut);margin-top:6px}
.tabla{overflow-x:auto;margin:16px 0 22px;-webkit-overflow-scrolling:touch}
table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.4}
thead th{background:var(--tinta);color:#fff;font:600 12px/1.25 var(--cuerpo);text-transform:uppercase;letter-spacing:.06em;text-align:left;padding:9px 10px;vertical-align:bottom}
td{padding:8px 10px;border-bottom:1px solid var(--linea);vertical-align:top}
tbody tr:nth-child(even) td{background:#faf8f7}
td:first-child{font-weight:600}
tr{break-inside:avoid}
.pie{border-top:1px solid var(--linea);padding:18px 40px 26px;font-size:12px;color:var(--mut);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.indice a{display:flex;gap:18px;align-items:baseline;text-decoration:none;color:inherit;padding:16px 0;border-bottom:1px solid var(--linea)}
.indice .n{font:700 44px/1 var(--disp);color:var(--rojo);min-width:56px}
.indice b{font:700 24px/1.1 var(--disp);display:block}
.indice span{color:var(--mut);font-size:15px}
@media (max-width:640px){
 .portada{padding:22px 16px 24px}.cuerpo{padding:22px 16px 36px}.pie{padding:16px}
 .titular{gap:14px}.num{font-size:72px}h1{font-size:34px}.pregunta{font-size:16px}
 h2{font-size:26px}table{font-size:13px}td,thead th{padding:7px 8px}}
@page{size:letter;margin:14mm 0 14mm 0}
@page:first{margin-top:0}
@media print{
 body{background:#fff;font-size:11pt}.hoja{box-shadow:none;max-width:none}
 .portada{-webkit-print-color-adjust:exact;print-color-adjust:exact}
 .cuerpo,.pie{padding-left:16mm;padding-right:16mm}.portada{padding-left:16mm;padding-right:16mm}
 h2,h3{break-after:avoid}h2{break-before:auto}
 blockquote,.tabla{break-inside:avoid}
 thead th,tbody tr:nth-child(even) td,blockquote,code{-webkit-print-color-adjust:exact;print-color-adjust:exact}
 a{color:var(--tinta);text-decoration:none}
 figure img{width:auto;max-width:100%;max-height:112mm;margin:0 auto}
 .tabla{overflow:visible}.pie{display:none}
 table.ancha{font-size:9pt}table.ancha td,table.ancha th{padding:6px 6px}}
table.ancha thead th{font-size:11px;letter-spacing:.03em}
"""

PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo_corto}</title>
<style>
{fuentes}
{css}
</style>
</head>
<body>
<div class="hoja">
<header class="portada">
 <div class="ceja"><span><b>Diablos Rojos del M&#233;xico</b> &#183; An&#225;lisis de pitcheo</span><span>{ceja}</span></div>
 <div class="titular"><div class="num">{num2}</div><h1>{titulo}</h1></div>
 <p class="pregunta">{pregunta}</p>
 <p class="meta">Modelo Stuff+ LMB 2024&#8211;2026 &#183; Estadio Alfredo Harp Hel&#250;, 2,240 m &#183; {fecha} &#183; {equipo}</p>
</header>
<main class="cuerpo">
{cuerpo}
</main>
<footer class="pie"><span>Hackathon ITAM / ISAC &#183; Stuff+ calibrado al Harp Hel&#250;</span><span>{equipo}</span></footer>
</div>
</body>
</html>
"""


def leer_md(p):
    s = p.read_text(encoding="utf-8-sig")
    m = re.match(r"---\n(.*?)\n---\n", s, re.S)
    meta = dict(l.split(": ", 1) for l in m.group(1).splitlines())
    return meta, s[m.end():]


def a_html(md):
    return subprocess.run(["pandoc", "-f", "gfm", "-t", "html5", "--wrap=none"],
                          input=md, capture_output=True, text=True, encoding="utf-8", check=True).stdout


def ajustar(cuerpo):
    # imagenes como figure con base64
    def img(m):
        src, alt = m.group(1), html.unescape(m.group(2))
        data = b64(MD / src)
        return (f'<figure><img src="data:image/png;base64,{data}" alt="{html.escape(alt)}"></figure>')
    cuerpo = re.sub(r'(?:<p>)?<img src="(?!data:)([^"]+)" alt="([^"]*)" ?/?>(?:</p>)?', img, cuerpo)
    def tabla(m):
        t = m.group(0)
        ancha = ' class="ancha"' if t.count("<th") >= 7 else ""
        return f'<div class="tabla"><table{ancha}>' + t[len("<table>"):]
    cuerpo = re.sub(r"<table>.*?</thead>", tabla, cuerpo, flags=re.S)
    cuerpo = cuerpo.replace("</table>", "</table></div>")
    # primer blockquote = resumen; los de "Ojo"/"aviso" en ámbar
    cuerpo = cuerpo.replace("<blockquote>", '<blockquote class="resumen">', 1)
    cuerpo = re.sub(r"<blockquote>\s*<p><strong>(Ojo|Un aviso)", r'<blockquote class="aviso">\n<p><strong>\1', cuerpo)
    return cuerpo


def ascii_html(s):
    # todo lo no ASCII como entidad, para que el acento sobreviva cualquier codificacion
    return "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in s)


def css_ascii(s):
    return "".join(c if ord(c) < 128 else "\\%06X " % ord(c) for c in s)


def construir():
    OUT.mkdir(exist_ok=True); PDF.mkdir(exist_ok=True)
    fuentes = fuentes_css()
    css = css_ascii(CSS)
    salidas, indice, partes = [], [], []
    mds = sorted(MD.glob("0[1-9]_*.md"))
    total = sum(1 for p in mds if "etiqueta" not in leer_md(p)[0])
    for p in mds:
        meta, md = leer_md(p)
        cuerpo = ajustar(a_html(md))
        num = int(meta["numero"])
        # los anexos llevan etiqueta (A, B...) en lugar de numero de reporte
        etq = meta.get("etiqueta")
        num2, ceja = (etq, f"Anexo {etq}") if etq else (f"{num:02d}", f"Reporte {num} de {total}")
        doc = PLANTILLA.format(titulo_corto=ascii_html(meta["titulo"]), fuentes=fuentes, css=css,
                               ceja=ceja, num2=num2, titulo=ascii_html(html.escape(meta["titulo"])),
                               pregunta=ascii_html(html.escape(meta["pregunta"])), fecha=FECHA,
                               equipo=ascii_html(EQUIPO), cuerpo=ascii_html(cuerpo))
        out = OUT / (p.stem + ".html")
        out.write_text(doc, encoding="ascii")
        salidas.append(out)
        indice.append((num, num2, meta["titulo"], meta["pregunta"], out.name))
        partes.append((num, num2, ceja, meta, cuerpo))
    # indice
    filas = "\n".join(
        f'<a href="{f}"><span class="n">{etq}</span><div><b>{html.escape(t)}</b><span>{html.escape(q)}</span></div></a>'
        for n, etq, t, q, f in indice)
    intro = ("<p>Cuatro reportes para la dirección deportiva y el cuerpo técnico, y dos anexos: el simulador y las referencias. "
             "Cada reporte abre con un resumen de 30 segundos y cierra con lo que significa para Diablos. Los números "
             "salen del modelo Stuff+ entrenado con los 629,616 pitcheos de la LMB 2024–2026.</p>"
             '<div class="indice">' + filas + "</div>"
             "<h2>Cómo leer los números</h2><ul><li><strong>Se lee como ERA+ u OPS+: 100 es el promedio de la LMB</strong> "
             "y más alto siempre es mejor para el pitcher; 120 o más es élite. La escala completa, con su equivalente "
             "en grados de scout, está al inicio del reporte 1.</li>"
             "<li><strong>Ambiente Harp Helú</strong> quiere decir: cómo quedaría cada pitcher en el ranking "
             "de la liga si todos lanzaran en el Harp Helú. Es como ajustar la efectividad por parque.</li>"
             "<li><strong>Los pitchers aparecen con su clave anónima</strong> de los datos de ISAC. Los equipos y "
             "estadios los inferimos por récord; ISAC no los ha confirmado.</li></ul>"
             "<h2>Cinco palabras que se repiten</h2><ul>"
             "<li><strong>Stuff+, Location+, Pitching+:</strong> qué tan buena es la bola, qué tan bien se ubicó "
             "y el pitcheo completo.</li>"
             "<li><strong>Bote (IVB, el “ride”):</strong> cuánto se resiste la recta a caer por el backspin. Una recta de 18 pulgadas parece que sube; "
             "una de 10 se ve “plana”.</li>"
             "<li><strong>Corrida (HB, el “run”):</strong> cuánto se mueve la pelota hacia los lados; en el cambio es el "
             "desvanecimiento.</li>"
             "<li><strong>Efecto Magnus:</strong> el empuje que da el giro y que produce el bote y la corrida. En el aire "
             "delgado de la Ciudad de México es más débil.</li>"
             "<li><strong>Castigo de altura:</strong> cuántas carreras de más permite un pitcheo en el Harp Helú "
             "contra el mismo pitcheo a nivel del mar.</li></ul>")
    doc = PLANTILLA.format(titulo_corto="Reportes Diablos", fuentes=fuentes, css=css, ceja="&#205;ndice", num2="00",
                           titulo="Stuff+ en el Harp Hel&#250;: reportes para la toma de decisiones",
                           pregunta=ascii_html("Qué vale cada pitcheo en casa, qué pitcher buscar y cómo usar la herramienta."),
                           fecha=FECHA, equipo=ascii_html(EQUIPO), cuerpo=ascii_html(intro))
    idx = OUT / "00_indice.html"
    idx.write_text(doc, encoding="ascii")
    completo(doc, indice, partes)
    return [idx] + salidas


SECCION = """<header class="portada sec" id="r{num}">
 <div class="ceja"><span><b>Diablos Rojos del M&#233;xico</b> &#183; An&#225;lisis de pitcheo</span><span>{ceja} &#183; <a class="volver" href="#indice">&#205;ndice &#8593;</a></span></div>
 <div class="titular"><div class="num">{num2}</div><h1>{titulo}</h1></div>
 <p class="pregunta">{pregunta}</p>
</header>
<main class="cuerpo">
{cuerpo}
</main>
"""

CSS_COMPLETO = """<style>
.portada.sec{margin-top:0}
.cuerpo + .portada.sec{border-top:10px solid var(--bg)}
.volver{color:#fff;text-decoration:none;border-bottom:1px solid #8a7f81}
html{scroll-behavior:smooth}
@media print{.portada.sec{break-before:page}.volver{display:none}}
</style>
</head>"""


def completo(doc_indice, indice, partes):
    """Un solo HTML: indice + los reportes y anexos, con ligas internas."""
    doc = doc_indice
    for n, etq, t, q, f in indice:
        doc = doc.replace(f'href="{f}"', f'href="#r{n}"')
    doc = doc.replace('<header class="portada">', '<header class="portada" id="indice">', 1)
    doc = doc.replace("</head>", CSS_COMPLETO, 1)
    secciones = "".join(SECCION.format(num=n, num2=num2, ceja=ceja, titulo=ascii_html(html.escape(m["titulo"])),
                                       pregunta=ascii_html(html.escape(m["pregunta"])), cuerpo=ascii_html(c))
                        for n, num2, ceja, m, c in partes)
    antes, despues = doc.split("</main>", 1)
    doc = antes + "</main>\n" + secciones + despues
    doc = doc.replace("<title>Reportes Diablos</title>", "<title>Reportes Diablos completos</title>")
    (OUT / "reportes_diablos_completo.html").write_text(doc, encoding="ascii")


def pdfs(htmls):
    from playwright.sync_api import sync_playwright
    from pypdf import PdfWriter
    pdfs = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        pg = b.new_page()
        for h in htmls:
            pg.goto(h.as_uri()); pg.wait_for_timeout(300)
            out = PDF / (h.stem + ".pdf")
            pg.pdf(path=str(out), format="Letter", print_background=True, prefer_css_page_size=True,
                   display_header_footer=True, header_template="<span></span>",
                   footer_template='<div style="width:100%;font:8px sans-serif;color:#8a8183;text-align:center">'
                                   '<span class="pageNumber"></span> / <span class="totalPages"></span></div>')
            pdfs.append(out)
        b.close()
    w = PdfWriter()
    for p in pdfs:
        w.append(str(p))
    w.write(str(PDF / "reportes_diablos_completo.pdf"))


if __name__ == "__main__":
    h = construir()
    if "--sin-pdf" not in sys.argv:
        pdfs(h)
    print("\n".join(str(x) for x in h))
