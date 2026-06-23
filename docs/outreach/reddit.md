# Drafts — Reddit posts

**Account caveat:** Post from your own account; space posts out (a few per day,
not all at once) to avoid spam filters. Read each sub's self-promo rules first.

## r/linux  /  r/linuxhardware
**Title:** I wrote a Linux driver + CUPS backend for the M08F A4 thermal printer (Phomemo/COLORWING/AIMO)

**Body:**
The M08F is a cheap A4 thermal printer with no Linux support. I reverse-engineered
its solid-red USB-serial ESC/POS mode and built a driver, CLI, and CUPS backend so
it prints from any app like a normal printer. MIT licensed, install script + AUR
package included. Repo: https://github.com/M-Wham/m08f-printer — feedback welcome.

## r/PrintersAndCopiers
**Title:** Got the M08F A4 thermal printer working on Linux (CUPS)

**Body:**
If you have an M08F (also branded Phomemo/COLORWING/AIMO) and a Linux box, it now
works as a real CUPS printer: https://github.com/M-Wham/m08f-printer. Includes a
probe/calibrate flow for the A4 width. Happy to help anyone who gets stuck.

## r/Phomemo  /  r/thermalprinter
**Title:** Open-source Linux driver for the M08F A4 (Phomemo-branded) thermal printer

**Body:**
Sharing in case it helps fellow owners — full Linux support (CLI + CUPS) for the
A4 M08F: https://github.com/M-Wham/m08f-printer. The existing phomemo-tools project
doesn't cover this A4 model, so this fills the gap. MIT licensed.
