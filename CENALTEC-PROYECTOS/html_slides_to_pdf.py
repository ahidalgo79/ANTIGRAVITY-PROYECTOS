"""
html_slides_to_pdf.py
Convierte presentaciones HTML (tipo deck/slider) a PDF de ultra alta calidad.
Resolución retina 2x (3840x2160 px efectivos por slide).

Requisitos:
    pip install playwright pypdf Pillow reportlab
    playwright install chromium

Uso:
    python html_slides_to_pdf.py

Ajusta las variables al final del script según tu caso.
"""

from playwright.sync_api import sync_playwright
from pypdf import PdfWriter, PdfReader
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import io, os


def html_slides_to_pdf(html_path: str, output_pdf: str, slide_count: int):
    """
    Abre un HTML de presentación en Chromium headless,
    activa cada slide uno por uno, toma screenshot en alta resolución
    y compila todo en un PDF.

    Args:
        html_path:    Ruta al archivo .html de la presentación.
        output_pdf:   Ruta de salida del PDF generado.
        slide_count:  Número total de slides en la presentación.
    """

    # ── 1. Capturar screenshots con Playwright ─────────────────────────────
    screenshots = []

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2,   # Retina / ultra alta calidad
        )
        page = context.new_page()

        file_url = f"file://{os.path.abspath(html_path)}"
        page.goto(file_url, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)   # espera extra para fuentes y animaciones

        for i in range(slide_count):
            # Activar slide i quitando la clase 'active' de todos
            # y asignándola solo al slide actual
            page.evaluate(f"""
                (() => {{
                    const slides = document.querySelectorAll('.slide');
                    slides.forEach((s, idx) => {{
                        s.classList.remove('active');
                        if (idx === {i}) s.classList.add('active');
                    }});
                }})()
            """)
            page.wait_for_timeout(300)   # pequeña pausa para que renderice

            img_path = f"/tmp/slide_{i:03d}.png"
            page.screenshot(path=img_path, full_page=False)
            screenshots.append(img_path)
            print(f"  Slide {i+1}/{slide_count} capturado", flush=True)

        browser.close()

    # ── 2. Ensamblar el PDF ────────────────────────────────────────────────
    writer = PdfWriter()

    # Dimensiones de página en puntos (pt) para 1920x1080 a 96 dpi
    # 1 pt = 1/72 in;  1 px a 96dpi = 72/96 pt
    pw = 1920 * 72 / 96   # 1440 pt
    ph = 1080 * 72 / 96   #  810 pt

    for img_path in screenshots:
        img = Image.open(img_path)
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Generar una página PDF con ReportLab
        page_buf = io.BytesIO()
        c = rl_canvas.Canvas(page_buf, pagesize=(pw, ph))
        c.drawImage(ImageReader(img), 0, 0, pw, ph)
        c.save()
        page_buf.seek(0)

        reader = PdfReader(page_buf)
        writer.add_page(reader.pages[0])

        os.remove(img_path)   # limpiar temporales

    with open(output_pdf, "wb") as f:
        writer.write(f)

    print(f"  ✓ PDF guardado: {output_pdf}")


# ── Configuración ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    trabajos = [
        {
            "html":        "presentacion_dia_1_v2.html",
            "output":      "presentacion_dia_1.pdf",
            "slide_count": 45,
        },
        {
            "html":        "presentacion_dia_2_v2.html",
            "output":      "presentacion_dia_2.pdf",
            "slide_count": 31,
        },
    ]

    for t in trabajos:
        print(f"\n=== {t['output']} ({t['slide_count']} slides) ===")
        html_slides_to_pdf(t["html"], t["output"], t["slide_count"])
