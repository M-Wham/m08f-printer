import pytest
from contextlib import contextmanager
from PIL import Image
from m08f import transport, printer

class FakeSerial:
    def __init__(self):
        self.written = bytearray()
        self.closed = False
    def write(self, data): self.written.extend(data); return len(data)
    def flush(self): pass
    def close(self): self.closed = True

def test_transport_writes_and_closes(monkeypatch):
    fake = FakeSerial()
    monkeypatch.setattr(transport.serial, "Serial", lambda *a, **k: fake)
    with transport.open_port("/dev/ttyACM0", 115200) as port:
        port.send(b"\x1b\x40")
    assert fake.written == b"\x1b\x40"
    assert fake.closed is True

def test_transport_device_missing_raises(monkeypatch):
    def boom(*a, **k):
        raise FileNotFoundError("no device")
    monkeypatch.setattr(transport.serial, "Serial", boom)
    with pytest.raises(transport.PrinterNotFound):
        with transport.open_port("/dev/ttyACM0", 115200):
            pass

def test_build_job_bytes_structure():
    img = Image.new("1", (16, 4), color=1)  # white
    opts = printer.Options(density=5, cut="Full", feed_lines=3, width_dots=16)
    data = printer.build_job(img, opts)
    assert data.startswith(b"\x1b\x40")
    assert b"\x1d\x28\x4b\x02\x00\x31\x05" in data
    assert b"\x1d\x76\x30" in data
    assert b"\x1b\x64\x03" in data
    assert b"\x1d\x56\x00" in data

def test_print_image_sends_built_bytes(monkeypatch):
    sent = bytearray()
    class P:
        def send(self, d): sent.extend(d)
        def close(self): pass
    @contextmanager
    def fake_open(device, baud):
        yield P()
    monkeypatch.setattr(printer.transport, "open_port", fake_open)
    img = Image.new("1", (16, 4), color=1)
    opts = printer.Options(density=3, cut="None", feed_lines=2, width_dots=16)
    printer.print_image(img, opts, device="/dev/ttyACM0", baud=115200)
    assert sent.startswith(b"\x1b\x40")
    assert len(sent) > 8
