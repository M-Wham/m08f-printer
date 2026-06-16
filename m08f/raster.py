"""Rasterize PDFs/images to ESC/POS raster blocks."""
import subprocess
import tempfile
from pathlib import Path
from PIL import Image

def image_to_blocks(img: Image.Image, width_dots: int, max_block_height: int = 255):
    """Return list of (width_bytes, height, data) tuples.

    Pillow mode "1": pixel value 0 = black, 255 = white.
    ESC/POS raster: bit 1 = print (black). So invert.
    """
    if img.mode != "1":
        img = img.convert("1")
    if img.width != width_dots:
        new_h = max(1, round(img.height * width_dots / img.width))
        img = img.resize((width_dots, new_h))
    width_bytes = (width_dots + 7) // 8
    px = img.load()
    blocks = []
    y = 0
    while y < img.height:
        h = min(max_block_height, img.height - y)
        buf = bytearray(width_bytes * h)
        for row in range(h):
            for x in range(img.width):
                if px[x, y + row] == 0:  # black -> set bit
                    buf[row * width_bytes + (x >> 3)] |= 0x80 >> (x & 7)
        blocks.append((width_bytes, h, bytes(buf)))
        y += h
    return blocks

def pdf_to_image(pdf_path: str, dpi: int) -> Image.Image:
    """Render all pages of a PDF to a single tall image via Ghostscript."""
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "page-%03d.png"
        subprocess.run(
            ["gs", "-dBATCH", "-dNOPAUSE", "-dSAFER", "-sDEVICE=pnggray",
             f"-r{dpi}", f"-sOutputFile={out}", pdf_path],
            check=True, capture_output=True,
        )
        pages = sorted(Path(td).glob("page-*.png"))
        if not pages:
            raise RuntimeError("Ghostscript produced no pages")
        imgs = [Image.open(p).convert("1") for p in pages]
        total_h = sum(i.height for i in imgs)
        w = max(i.width for i in imgs)
        canvas = Image.new("1", (w, total_h), color=1)
        y = 0
        for i in imgs:
            canvas.paste(i, (0, y))
            y += i.height
        return canvas

def load_source(path: str, dpi: int) -> Image.Image:
    """Dispatch by extension: PDF via gs, images via Pillow."""
    if path.lower().endswith(".pdf"):
        return pdf_to_image(path, dpi)
    return Image.open(path).convert("1")
