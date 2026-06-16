"""Serial transport. Only layer that touches the port."""
import serial
from contextlib import contextmanager

class PrinterNotFound(Exception):
    pass

class Port:
    def __init__(self, ser):
        self._ser = ser
    def send(self, data: bytes) -> None:
        self._ser.write(data)
        self._ser.flush()
    def close(self) -> None:
        self._ser.close()

@contextmanager
def open_port(device: str, baud: int):
    try:
        ser = serial.Serial(device, baud, timeout=2)
    except (FileNotFoundError, OSError) as e:
        raise PrinterNotFound(
            f"Printer not detected at {device}. "
            "Switch printer to solid red mode and check the cable."
        ) from e
    port = Port(ser)
    try:
        yield port
    finally:
        port.close()
