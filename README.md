# m08f-printer

Linux driver, CLI, and CUPS backend for the M08F A4 thermal printer — sold as the
Phomemo M08F, COLORWING M08F, and AIMO M08F (all USB `0483:5740`).

The printer enumerates as a USB serial port (`/dev/ttyACM0`) only in solid-red mode: hold
power ~3s until the light is solid red before use.

## Requirements

Python 3.9+, `ghostscript`, and CUPS.

```bash
sudo pacman -S ghostscript cups      # Arch
# sudo apt install ghostscript cups  # Debian/Ubuntu
sudo systemctl enable --now cups
```

## Install

```bash
git clone https://github.com/mwham/m08f-printer && cd m08f-printer
python3 -m venv .venv
.venv/bin/pip install -e .

# udev rule: device access without sudo (re-login after usermod)
sudo cp udev/99-m08f.rules /etc/udev/rules.d/
sudo usermod -aG uucp $USER
sudo udevadm control --reload && sudo udevadm trigger
newgrp uucp

.venv/bin/m08f probe                 # detect baud; answer y when a clean bar prints
.venv/bin/m08f calibrate             # printable width; enter 1677 for A4 @ 203 DPI

# CUPS backend: __M08F_BIN__ is replaced with the absolute path to the m08f binary
sudo sed "s|__M08F_BIN__|$(pwd)/.venv/bin/m08f|" cups/m08f-backend \
    | sudo tee /usr/lib/cups/backend/m08f > /dev/null
sudo chmod 700 /usr/lib/cups/backend/m08f
sudo lpadmin -p M08F -E -v m08f:/dev/m08f -P cups/m08f.ppd
sudo cupsenable M08F && sudo cupsaccept M08F
```

For a system-wide install (e.g. `pipx`), use `$(command -v m08f)` in place of the `sed` path.

## Usage

```bash
.venv/bin/m08f print file.pdf --density 6 --cut Full --feed 4
.venv/bin/m08f print image.png
.venv/bin/m08f status
```

Or print from any app: select M08F and adjust density/cut/feed in the print dialog.

## Options

| CLI / CUPS | Values | Default |
|---|---|---|
| `--density` / `PrintDensity` | 1–8 | 5 |
| `--cut` / `PaperCut` | None, Partial, Full | None |
| `--feed` / `LineFeed` | 0–10 lines | 3 |

## Troubleshooting

- Not detected — printer not in solid-red mode, or you're not in `uucp` (`newgrp uucp`).
- Job stuck — check `sudo tail /var/log/cups/error_log`.
- Faint output — raise `--density` (7–8); dark/smeared — lower it (3–4).
- Text too small — print a PDF, not a PNG, so DPI scaling applies.

## Hardware

USB `0483:5740` (STM32 VCP) · 203 DPI · A4, printable width 1677 dots.
Solid red = USB data mode; flashing = no USB enumeration.

Packaging (AUR, `.deb`, install script) is planned.
