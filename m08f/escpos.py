"""ESC/POS byte-sequence builders. Pure functions, return bytes."""

def initialize() -> bytes:
    return b"\x1b\x40"

def feed(lines: int) -> bytes:
    lines = max(0, min(255, int(lines)))
    return b"\x1b\x64" + bytes([lines])

def cut(mode: str) -> bytes:
    if mode == "Full":
        return b"\x1d\x56\x00"
    if mode == "Partial":
        return b"\x1d\x56\x01"
    return b""

def density(level: int) -> bytes:
    level = max(1, min(8, int(level)))
    # GS ( K  pL pH fn m  -> pL=2 pH=0 fn=49 m=level
    return b"\x1d\x28\x4b\x02\x00\x31" + bytes([level])

def raster_block(width_bytes: int, height: int, data: bytes) -> bytes:
    xL, xH = width_bytes & 0xFF, (width_bytes >> 8) & 0xFF
    yL, yH = height & 0xFF, (height >> 8) & 0xFF
    header = b"\x1d\x76\x30" + bytes([0, xL, xH, yL, yH])
    return header + data
