#!/usr/bin/env bash
# repo-setup.sh — post-publish repo chores that require YOUR GitHub auth.
# The agent cannot (and must not) run these for you. Review, then run:
#     ./scripts/repo-setup.sh
# Requires: gh (authenticated: `gh auth status`), and for sums: pacman-contrib.
set -euo pipefail

REPO="M-Wham/m08f-printer"
TOPICS=(thermal-printer phomemo m08f cups escpos linux printer-driver colorwing aimo)

confirm() { read -r -p "$1 [y/N] " a; [ "$a" = "y" ] || [ "$a" = "Y" ]; }

echo "== 1. GitHub repo topics =="
echo "Will set topics on $REPO: ${TOPICS[*]}"
if confirm "Apply topics?"; then
    gh repo edit "$REPO" $(printf -- '--add-topic %s ' "${TOPICS[@]}")
    echo "  topics applied."
else
    echo "  skipped."
fi

echo
echo "== 2. AUR sha256sums (run AFTER the v0.1.0 GitHub release tag exists) =="
echo "Regenerates checksums in packaging/aur/PKGBUILD from the released tarball."
if confirm "Run updpkgsums now?"; then
    if command -v updpkgsums >/dev/null; then
        ( cd packaging/aur && updpkgsums )
        echo "  PKGBUILD checksums updated — review the diff before committing."
    else
        echo "  updpkgsums not found (install pacman-contrib). Skipped."
    fi
else
    echo "  skipped."
fi

echo
echo "Done. Nothing was pushed. Review any changed files, then commit/push yourself."
