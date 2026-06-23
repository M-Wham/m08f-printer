# Draft — OpenPrinting printer DB submission

**Where:** https://openprinting.org/printers (use "Add a printer" / submit form)
**Goal:** M08F shows up in "does my printer work on Linux" searches.

**Fields to submit:**
- Manufacturer: Phomemo (note aliases COLORWING, AIMO in comments)
- Model: M08F (A4 thermal)
- Connection: USB (CDC/ACM), USB id 0483:5740
- Driver: m08f-printer (CUPS backend + PPD)
- Driver URL: https://github.com/M-Wham/m08f-printer
- Works: Yes (mono raster, A4 @ 203 DPI)
- License: MIT
- Notes: Printer must be in "solid red" USB-serial mode. CLI provides
  probe/calibrate; CUPS backend exposes PrintDensity/PaperCut/LineFeed options.
