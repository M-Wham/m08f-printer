# AUR Package (m08f-printer) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a complete, test-built versioned AUR package (`PKGBUILD` + `.SRCINFO`) for `m08f-printer` under `packaging/aur/`, plus fix the wrong GitHub URLs in the docs.

**Architecture:** A pure-Python (`arch=any`) AUR package built from the GitHub release tarball for tag `v0.1.0`. It builds a wheel via PEP 517 (`python-build` → `python-installer`) and additionally installs the udev rule, CUPS backend (with the `__M08F_BIN__` placeholder rewritten to `/usr/bin/m08f`), the PPD, and the license. Reproducible via a real `sha256sum` (never `SKIP`).

**Tech Stack:** Bash PKGBUILD, `makepkg`, Python PEP 517 packaging, CUPS, udev.

**Reference spec:** `docs/superpowers/specs/2026-06-18-aur-package-design.md`

---

## ⚠️ PRECONDITION — must be true before running this plan

The git tag **`v0.1.0`** must already be pushed to `github.com/M-Wham/m08f-printer`, so that this URL returns a `200`:

```
https://github.com/M-Wham/m08f-printer/archive/refs/tags/v0.1.0.tar.gz
```

Verify before starting:

```bash
curl -sIL -o /dev/null -w '%{http_code}\n' \
  https://github.com/M-Wham/m08f-printer/archive/refs/tags/v0.1.0.tar.gz
```

Expected: `200`. If it returns `404`, **stop** — the human must `git tag v0.1.0 && git push origin v0.1.0` first (the sandbox has no GitHub push auth). Without the tag, Task 4 (checksum) cannot complete.

All paths below are relative to the repo root.

---

## Task 1: Fix the wrong GitHub URLs in the docs

The README and `pyproject.toml` point at `github.com/mwham/...` (a nonexistent account). The real repo is `github.com/M-Wham/...`. (The `name = "mwham"` author field in pyproject is a display name — leave it.)

**Files:**
- Modify: `pyproject.toml:33-35`
- Modify: `README.md:22`

- [ ] **Step 1: Fix the three URLs in pyproject.toml**

Replace lines 33-35:

```toml
Homepage = "https://github.com/M-Wham/m08f-printer"
Repository = "https://github.com/M-Wham/m08f-printer"
Issues = "https://github.com/M-Wham/m08f-printer/issues"
```

- [ ] **Step 2: Fix the clone URL in README.md**

Replace the `git clone` line (line 22):

```bash
git clone https://github.com/M-Wham/m08f-printer && cd m08f-printer
```

- [ ] **Step 3: Verify no wrong URLs remain**

Run:

```bash
grep -rn "github.com/mwham/" README.md pyproject.toml
```

Expected: no output (exit code 1). If any line prints, fix it.

- [ ] **Step 4: Commit**

```bash
git add README.md pyproject.toml
git commit -m "fix: correct GitHub URLs to M-Wham account"
```

---

## Task 2: Create the PKGBUILD

**Files:**
- Create: `packaging/aur/PKGBUILD`

- [ ] **Step 1: Create the directory**

```bash
mkdir -p packaging/aur
```

- [ ] **Step 2: Write `packaging/aur/PKGBUILD`**

Write this exact content. The `sha256sums` line intentionally holds a placeholder that Task 4 replaces — do not commit it as-is.

```bash
# Maintainer: mwham <mwams-mail@proton.me>
pkgname=m08f-printer
pkgver=0.1.0
pkgrel=1
pkgdesc="Linux driver/CLI/CUPS backend for the M08F A4 thermal printer (Phomemo / COLORWING / AIMO)"
arch=('any')
url="https://github.com/M-Wham/m08f-printer"
license=('MIT')
depends=('python' 'python-pyserial' 'python-pillow' 'ghostscript' 'cups')
makedepends=('python-build' 'python-installer' 'python-wheel' 'python-setuptools')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
    cd "$srcdir/$pkgname-$pkgver"
    python -m build --wheel --no-isolation
}

package() {
    cd "$srcdir/$pkgname-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl

    # udev rule (device access without sudo)
    install -Dm644 udev/99-m08f.rules \
        "$pkgdir/usr/lib/udev/rules.d/99-m08f.rules"

    # CUPS backend: rewrite the build-time placeholder to the installed binary
    # path. CUPS requires backend mode 700.
    install -dm755 "$pkgdir/usr/lib/cups/backend"
    sed 's|__M08F_BIN__|/usr/bin/m08f|' cups/m08f-backend \
        > "$pkgdir/usr/lib/cups/backend/m08f"
    chmod 700 "$pkgdir/usr/lib/cups/backend/m08f"

    # CUPS PPD
    install -Dm644 cups/m08f.ppd "$pkgdir/usr/share/cups/model/m08f.ppd"

    # License
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
```

> Note: `sha256sums=('SKIP')` is a temporary value so `makepkg -g` in Task 4 can download the source. It MUST be replaced with the real hash before committing (Task 4).

- [ ] **Step 3: Verify the PKGBUILD parses**

Run:

```bash
cd packaging/aur && bash -n PKGBUILD && echo PARSE_OK; cd ../..
```

Expected: `PARSE_OK` (no syntax errors).

---

## Task 3: Confirm the release tarball is reachable

**Files:** none (verification only)

- [ ] **Step 1: Re-check the tarball URL resolves**

Run:

```bash
curl -sIL -o /dev/null -w '%{http_code}\n' \
  https://github.com/M-Wham/m08f-printer/archive/refs/tags/v0.1.0.tar.gz
```

Expected: `200`. If `404`, the precondition is unmet — stop and report that the human must push tag `v0.1.0`.

---

## Task 4: Compute and fill in the real sha256sum

**Files:**
- Modify: `packaging/aur/PKGBUILD` (the `sha256sums` line)

- [ ] **Step 1: Download the source and compute the real checksum via makepkg**

Run from the package dir:

```bash
cd packaging/aur && makepkg -g
```

Expected: prints one line like `sha256sums=('a1b2c3...64hexchars...')`. This is `makepkg` downloading the real tarball and hashing it.

> Fallback if `makepkg -g` fails (e.g. network helper issues): compute directly —
> ```bash
> curl -L -o /tmp/m08f-0.1.0.tar.gz \
>   https://github.com/M-Wham/m08f-printer/archive/refs/tags/v0.1.0.tar.gz
> sha256sum /tmp/m08f-0.1.0.tar.gz
> ```
> Use the resulting 64-char hex in the next step.

- [ ] **Step 2: Replace the placeholder with the real hash**

In `packaging/aur/PKGBUILD`, replace the line `sha256sums=('SKIP')` with the exact line printed in Step 1, e.g.:

```bash
sha256sums=('<the 64-char hex from Step 1>')
```

- [ ] **Step 3: Verify no SKIP remains and the source verifies**

Run:

```bash
cd packaging/aur && grep -q "SKIP" PKGBUILD && echo "SKIP STILL PRESENT - FIX" || echo "no SKIP - good"
makepkg --verifysource
cd ../..
```

Expected: `no SKIP - good`, and `makepkg --verifysource` ends without a checksum mismatch error (it re-downloads if needed and validates).

---

## Task 5: Test-build the package

`makepkg` cannot run as root and needs the `makedepends` available.

**Files:** none (verification only; build artifacts are not committed)

- [ ] **Step 1: Ensure build dependencies are present**

Run:

```bash
python -c "import build, installer" 2>/dev/null && echo "build deps present" || echo "build deps MISSING"
```

If MISSING, install the Arch packages (preferred):

```bash
sudo pacman -S --needed --asdeps python-build python-installer python-wheel python-setuptools
```

If `sudo`/pacman is unavailable in the sandbox, install into the user environment as a fallback so `makepkg --nodeps` can build:

```bash
python -m pip install --user build installer wheel setuptools
```

- [ ] **Step 2: Build the package**

Run from the package dir:

```bash
cd packaging/aur && makepkg -f --noconfirm; cd ../..
```

If `makedepends` could not be installed system-wide and you used the pip fallback, build with `--nodeps` instead:

```bash
cd packaging/aur && makepkg -f --nodeps --noconfirm; cd ../..
```

Expected: ends with `Finished making: m08f-printer` and produces a file matching `packaging/aur/m08f-printer-0.1.0-1-any.pkg.tar.zst`.

- [ ] **Step 3: Confirm the built package exists**

Run:

```bash
ls packaging/aur/m08f-printer-0.1.0-1-any.pkg.tar.zst
```

Expected: the path prints (file exists).

- [ ] **Step 4: (Optional) Lint with namcap**

`namcap` is not guaranteed to be installed. Run it only if present:

```bash
command -v namcap >/dev/null && namcap packaging/aur/PKGBUILD packaging/aur/m08f-printer-0.1.0-1-any.pkg.tar.zst || echo "namcap not installed - skipping lint"
```

Expected: either namcap output (review any warnings; "no missing/unused dependency" findings are advisory) or `namcap not installed - skipping lint`. Do not block on its absence.

---

## Task 6: Verify package contents land at the right paths

**Files:** none (verification only)

- [ ] **Step 1: List the package contents**

Run:

```bash
bsdtar tf packaging/aur/m08f-printer-0.1.0-1-any.pkg.tar.zst | grep -vE '^\.(PKGINFO|BUILDINFO|MTREE)$'
```

Expected output to include all of these entries (paths relative to `/`):

```
usr/bin/m08f
usr/lib/python3.*/site-packages/m08f/
usr/lib/udev/rules.d/99-m08f.rules
usr/lib/cups/backend/m08f
usr/share/cups/model/m08f.ppd
usr/share/licenses/m08f-printer/LICENSE
```

If any entry is missing, the corresponding `install`/`sed` line in `package()` is wrong — fix `packaging/aur/PKGBUILD` and re-run Task 5.

- [ ] **Step 2: Confirm the CUPS backend placeholder was substituted**

Run:

```bash
bsdtar xOf packaging/aur/m08f-printer-0.1.0-1-any.pkg.tar.zst usr/lib/cups/backend/m08f | grep -n "exec /usr/bin/m08f print"
```

Expected: matches the `exec /usr/bin/m08f print ...` line (i.e. `__M08F_BIN__` is gone, replaced by `/usr/bin/m08f`).

Confirm the placeholder is absent:

```bash
bsdtar xOf packaging/aur/m08f-printer-0.1.0-1-any.pkg.tar.zst usr/lib/cups/backend/m08f | grep -c "__M08F_BIN__"
```

Expected: `0`.

---

## Task 7: Generate .SRCINFO

The AUR requires a `.SRCINFO` generated from the finished PKGBUILD.

**Files:**
- Create: `packaging/aur/.SRCINFO`

- [ ] **Step 1: Generate it**

Run from the package dir:

```bash
cd packaging/aur && makepkg --printsrcinfo > .SRCINFO; cd ../..
```

- [ ] **Step 2: Sanity-check it**

Run:

```bash
grep -E "pkgname = m08f-printer|pkgver = 0.1.0|sha256sums =" packaging/aur/.SRCINFO
```

Expected: shows the `pkgname`, `pkgver = 0.1.0`, and a `sha256sums =` line carrying the real hash (not `SKIP`).

---

## Task 8: Clean up build artifacts and commit

`makepkg` leaves `src/`, `pkg/`, the downloaded tarball, and the `.pkg.tar.zst` in `packaging/aur/`. None of these belong in git — only `PKGBUILD` and `.SRCINFO` do.

**Files:**
- Create: `packaging/aur/.gitignore`
- Commit: `packaging/aur/PKGBUILD`, `packaging/aur/.SRCINFO`, `packaging/aur/.gitignore`

- [ ] **Step 1: Add a .gitignore for build artifacts**

Write `packaging/aur/.gitignore`:

```gitignore
# makepkg build artifacts
src/
pkg/
*.tar.gz
*.pkg.tar.zst
```

- [ ] **Step 2: Confirm only the intended files are staged**

Run:

```bash
git add packaging/aur/PKGBUILD packaging/aur/.SRCINFO packaging/aur/.gitignore
git status --short packaging/aur/
```

Expected: only `PKGBUILD`, `.SRCINFO`, and `.gitignore` show as staged (`A`); no `src/`, `pkg/`, or tarball/zst files.

- [ ] **Step 3: Commit**

```bash
git commit -m "feat: add AUR package (PKGBUILD + .SRCINFO)"
```

---

## Task 9: Document the AUR publish procedure (human-only step)

The actual `git push` to the AUR needs the maintainer's AUR SSH key and cannot run in the sandbox. Capture the procedure so the human can finish.

**Files:**
- Create: `packaging/aur/PUBLISHING.md`

- [ ] **Step 1: Write `packaging/aur/PUBLISHING.md`**

```markdown
# Publishing m08f-printer to the AUR

These steps run on the maintainer's machine with an AUR account and SSH key
registered at https://aur.archlinux.org (My Account → SSH Public Key).

1. Clone the (empty, on first publish) AUR repo:

       git clone ssh://aur@aur.archlinux.org/m08f-printer.git aur-m08f-printer

2. Copy the package files in (the AUR repo holds PKGBUILD + .SRCINFO at its root):

       cp packaging/aur/PKGBUILD packaging/aur/.SRCINFO aur-m08f-printer/

3. From inside the AUR clone, verify and push:

       cd aur-m08f-printer
       makepkg --printsrcinfo > .SRCINFO   # regenerate to be safe
       git add PKGBUILD .SRCINFO
       git commit -m "Initial upload: m08f-printer 0.1.0"
       git push

## Updating for a new release

1. Bump `pkgver` (and reset `pkgrel=1`) in `packaging/aur/PKGBUILD`.
2. Push the matching `vX.Y.Z` git tag to github.com/M-Wham/m08f-printer.
3. `cd packaging/aur && makepkg -g` and paste the new `sha256sums` line in.
4. `makepkg --printsrcinfo > .SRCINFO`.
5. Commit both files here, then copy into the AUR clone and `git push`.
```

- [ ] **Step 2: Commit**

```bash
git add packaging/aur/PUBLISHING.md
git commit -m "docs: add AUR publishing procedure"
```

---

## Done criteria

- `packaging/aur/PKGBUILD` builds a `m08f-printer-0.1.0-1-any.pkg.tar.zst` with a real (non-`SKIP`) sha256sum.
- The package installs `usr/bin/m08f`, the Python module, the udev rule, the CUPS backend (with `/usr/bin/m08f` substituted), the PPD, and the license at the documented paths.
- `packaging/aur/.SRCINFO` is generated and consistent with the PKGBUILD.
- Wrong `mwham` URLs are gone from README and pyproject.
- `packaging/aur/PUBLISHING.md` documents the human push-to-AUR step.
