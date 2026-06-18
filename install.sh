#!/usr/bin/env bash
# install.sh — m08f-printer installer (any distro)
# Usage: sudo ./install.sh [USERNAME]
#   USERNAME defaults to the user who invoked sudo.
#
# Installs an isolated venv to /opt/m08f-printer, symlinks the m08f binary to
# /usr/local/bin/m08f, installs the udev rule, adds the user to the uucp group,
# and registers the printer with CUPS.
set -euo pipefail

INSTALL_DIR="/opt/m08f-printer"
BIN_LINK="/usr/local/bin/m08f"
UDEV_RULE="/etc/udev/rules.d/99-m08f.rules"
CUPS_BACKEND="/usr/lib/cups/backend/m08f"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_USER="${1:-${SUDO_USER:-$(logname 2>/dev/null || true)}}"

if [[ "$EUID" -ne 0 ]]; then
    echo "Run with sudo: sudo ./install.sh" >&2
    exit 1
fi

if [[ -z "$TARGET_USER" || "$TARGET_USER" == "root" ]]; then
    echo "Could not determine target user. Pass it explicitly: sudo ./install.sh <username>" >&2
    exit 1
fi

echo "==> Checking dependencies ..."
missing=()
for cmd in python3 gs lpadmin udevadm; do
    command -v "$cmd" &>/dev/null || missing+=("$cmd")
done
if [[ ${#missing[@]} -gt 0 ]]; then
    echo "Missing: ${missing[*]}" >&2
    echo "Install the ghostscript and cups packages first (see README Requirements)." >&2
    exit 1
fi

echo "==> Installing Python package to $INSTALL_DIR ..."
python3 -m venv "$INSTALL_DIR"
"$INSTALL_DIR/bin/pip" install --quiet --upgrade pip
"$INSTALL_DIR/bin/pip" install --quiet "$SCRIPT_DIR"

echo "==> Linking binary to $BIN_LINK ..."
ln -sf "$INSTALL_DIR/bin/m08f" "$BIN_LINK"

echo "==> Installing udev rule ..."
install -Dm644 "$SCRIPT_DIR/udev/99-m08f.rules" "$UDEV_RULE"
udevadm control --reload
udevadm trigger

echo "==> Adding $TARGET_USER to uucp group ..."
usermod -aG uucp "$TARGET_USER"

echo "==> Installing CUPS backend ..."
# The shipped backend contains the __M08F_BIN__ placeholder; point it at the symlink.
sed "s|__M08F_BIN__|$BIN_LINK|" "$SCRIPT_DIR/cups/m08f-backend" > "$CUPS_BACKEND"
if grep -q '__M08F_BIN__' "$CUPS_BACKEND"; then
    echo "Failed to substitute backend binary path." >&2
    exit 1
fi
chown root:root "$CUPS_BACKEND"
chmod 700 "$CUPS_BACKEND"

echo "==> Registering printer in CUPS ..."
lpadmin -p M08F -E -v m08f:/dev/m08f -P "$SCRIPT_DIR/cups/m08f.ppd"
cupsenable M08F
cupsaccept M08F

cat <<EOF

Install complete.
  1. Log out and back in (or run: newgrp uucp) so the uucp group applies.
  2. Switch the printer to solid red mode (hold power ~3s).
  3. Run: m08f probe      # detects baud, prints a test bar
  4. Run: m08f calibrate  # enter 1677 for A4 at 203 DPI
  5. Print from any app and select the "M08F" printer.

Remove with: sudo ./uninstall.sh
EOF
