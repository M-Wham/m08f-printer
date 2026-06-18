#!/usr/bin/env bash
# uninstall.sh — remove m08f-printer (reverses install.sh)
# Usage: sudo ./uninstall.sh
set -euo pipefail

if [[ "$EUID" -ne 0 ]]; then
    echo "Run with sudo: sudo ./uninstall.sh" >&2
    exit 1
fi

echo "==> Removing CUPS printer ..."
lpadmin -x M08F 2>/dev/null || echo "  (printer not registered, skipping)"

echo "==> Removing CUPS backend ..."
rm -f /usr/lib/cups/backend/m08f

echo "==> Removing binary symlink ..."
rm -f /usr/local/bin/m08f

echo "==> Removing install directory ..."
rm -rf /opt/m08f-printer

echo "==> Removing udev rule ..."
rm -f /etc/udev/rules.d/99-m08f.rules
udevadm control --reload
udevadm trigger

cat <<'EOF'

Uninstall complete.
Your user was NOT removed from the uucp group. To remove it:
  sudo gpasswd -d <username> uucp
EOF
