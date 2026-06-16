from PIL import Image
from m08f import raster

def test_image_to_rows_packs_width_to_bytes():
    img = Image.new("1", (16, 2), color=0)  # 0 = black in mode "1"
    blocks = raster.image_to_blocks(img, width_dots=16)
    assert len(blocks) == 1
    wb, h, data = blocks[0]
    assert wb == 2
    assert h == 2
    assert data == b"\xff\xff\xff\xff"

def test_image_scaled_to_width():
    img = Image.new("1", (32, 4), color=1)  # white
    blocks = raster.image_to_blocks(img, width_dots=16)
    wb, h, data = blocks[0]
    assert wb == 2
    assert data == b"\x00" * (2 * h)

def test_chunks_tall_image_into_multiple_blocks():
    img = Image.new("1", (16, 500), color=1)
    blocks = raster.image_to_blocks(img, width_dots=16, max_block_height=255)
    assert len(blocks) == 2
    assert blocks[0][1] == 255
    assert blocks[1][1] == 245
