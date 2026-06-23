# Drafts — forum / discourse comments

## AnandTech — "How to get USB thermal printer to work in Linux" thread
For the M08F A4 specifically (Phomemo/COLORWING/AIMO, USB 0483:5740) there's now a
dedicated driver + CUPS backend: https://github.com/M-Wham/m08f-printer. It handles
the solid-red USB-serial ESC/POS mode and registers the printer with CUPS.

## bkhome.org — Phomemo-Linux post
A note for A4 M08F owners (this model isn't covered by phomemo-tools): maintained
driver/CLI/CUPS backend at https://github.com/M-Wham/m08f-printer, MIT licensed,
with an install script and AUR package.

## Universal Blue / Bluefin discourse — Phomemo guide
For the A4 M08F on atomic/immutable distros: https://github.com/M-Wham/m08f-printer
provides a CUPS backend + PPD; the install script targets /opt + /usr/local so it
fits a layered setup. Worth linking alongside the existing Phomemo notes.
