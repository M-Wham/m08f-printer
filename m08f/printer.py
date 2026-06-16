"""Orchestrate a print job: options -> raster -> escpos -> transport."""
from dataclasses import dataclass
from PIL import Image
from m08f import escpos, raster, transport

@dataclass
class Options:
    density: int = 5
    cut: str = "None"
    feed_lines: int = 3
    width_dots: int = 1664

def build_job(img: Image.Image, opts: Options) -> bytes:
    out = bytearray()
    out += escpos.initialize()
    out += escpos.density(opts.density)
    for width_bytes, height, data in raster.image_to_blocks(img, opts.width_dots):
        out += escpos.raster_block(width_bytes, height, data)
    out += escpos.feed(opts.feed_lines)
    out += escpos.cut(opts.cut)
    return bytes(out)

def print_image(img: Image.Image, opts: Options, device: str, baud: int) -> None:
    data = build_job(img, opts)
    with transport.open_port(device, baud) as port:
        port.send(data)

def print_file(path: str, opts: Options, device: str, baud: int, dpi: int) -> None:
    img = raster.load_source(path, dpi)
    print_image(img, opts, device, baud)
