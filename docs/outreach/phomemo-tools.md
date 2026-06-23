# Draft — vivier/phomemo-tools issue or PR

**Where:** https://github.com/vivier/phomemo-tools/issues (open an issue; offer a PR)
**Goal:** Get the A4 M08F linked from the canonical Phomemo Linux project.

---

**Title:** Add support/link for the M08F A4 thermal printer (USB 0483:5740)

**Body:**

phomemo-tools is the go-to project for Phomemo printers on Linux, but it doesn't
cover the **M08F A4** thermal printer (sold as Phomemo / COLORWING / AIMO,
USB id `0483:5740`). It's a different beast from the label printers here: A4
width, USB CDC/ACM in "solid red" mode, ESC/POS raster.

I wrote a standalone driver + CLI + CUPS backend for it:
https://github.com/M-Wham/m08f-printer

Happy to either (a) add a note/link to this repo's README pointing M08F owners to
it, or (b) discuss folding the A4 path in here if you'd prefer it consolidated.
Which do you prefer?
