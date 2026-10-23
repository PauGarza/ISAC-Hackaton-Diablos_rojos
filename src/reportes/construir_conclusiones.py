"""Construye reports/resumen_ejecutivo/reporte_conclusiones.{html,pdf} a partir de reporte_conclusiones.md.

Uso: python construir_conclusiones.py
Necesita pandoc y Playwright con un Chromium local (mismo CHROME que construir_reportes.py).
"""
import subprocess
from pathlib import Path

from construir_reportes import CHROME, ascii_html

ENT = Path(__file__).resolve().parents[2] / "reports" / "resumen_ejecutivo"
MD, HTML, PDF = (ENT / f"reporte_conclusiones.{e}" for e in ("md", "html", "pdf"))

ESTILO = """<style type="text/css">body{margin:0;background:#fff;color:#1d2330;font:15px/1.6 -apple-system,"Segoe UI",Helvetica,Arial,sans-serif}
main,body>*{max-width:820px;margin-left:auto;margin-right:auto;padding-left:16px;padding-right:16px}
h1{font-size:27px;margin-top:32px} h2{font-size:20px;margin-top:34px;border-bottom:2px solid #c8102e;padding-bottom:4px} h3{font-size:16.5px}
img{max-width:100%;height:auto;display:block;margin:14px auto 4px}
table{border-collapse:collapse;width:calc(100% - 32px);max-width:788px;font-size:13px;margin:14px auto;display:table;padding:0!important}
@media (max-width:600px){table{display:block;overflow-x:auto;width:calc(100% - 32px)!important;max-width:none;margin:14px 16px}}
code{overflow-wrap:anywhere}
th,td{border-bottom:1px solid #e3e6eb;padding:6px 7px;text-align:left;vertical-align:top} th{background:#f5f6f8}
code{background:#f3f4f6;padding:1px 4px;border-radius:3px;font-size:13px} em{color:#5b6473}
@media print{body{font-size:12.5px}table,img{break-inside:avoid} img{max-height:95mm;width:auto} h2,h3{break-after:avoid}}
</style>
"""


def construir():
    cab = ENT / "_estilo_conclusiones.html"
    cab.write_text(ESTILO, encoding="utf-8")
    try:
        html = subprocess.run(
            ["pandoc", MD.name, "-f", "markdown-implicit_figures-citations", "-t", "html5", "-s", "--embed-resources",
             "--metadata", "pagetitle=Reporte de conclusiones Stuff+", "-H", cab.name],
            cwd=ENT, capture_output=True, text=True, encoding="utf-8", check=True).stdout
    finally:
        cab.unlink()
    HTML.write_text(ascii_html(html), encoding="ascii")


def pdf():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        pg = b.new_page()
        pg.goto(HTML.as_uri()); pg.wait_for_timeout(300)
        pg.pdf(path=str(PDF), format="Letter", print_background=True,
               margin={"top": "14mm", "bottom": "14mm", "left": "10mm", "right": "10mm"})
        b.close()


if __name__ == "__main__":
    construir()
    pdf()
    print(HTML, PDF, sep="\n")
