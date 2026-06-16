from m08f import escpos

def test_initialize():
    assert escpos.initialize() == b"\x1b\x40"

def test_feed_lines():
    assert escpos.feed(3) == b"\x1b\x64\x03"

def test_cut_full():
    assert escpos.cut("Full") == b"\x1d\x56\x00"

def test_cut_partial():
    assert escpos.cut("Partial") == b"\x1d\x56\x01"

def test_cut_none_is_empty():
    assert escpos.cut("None") == b""

def test_raster_line_header_dimensions():
    row = bytes([0b10101010])
    out = escpos.raster_block(width_bytes=1, height=1, data=row)
    assert out[:3] == b"\x1d\x76\x30"
    assert out[3] == 0
    assert out[4] == 1
    assert out[5] == 0
    assert out[6] == 1
    assert out[7] == 0
    assert out[8:] == row

def test_density_in_range():
    out = escpos.density(5)
    assert isinstance(out, bytes) and len(out) > 0

def test_density_clamps():
    assert escpos.density(99) == escpos.density(8)
    assert escpos.density(0) == escpos.density(1)
