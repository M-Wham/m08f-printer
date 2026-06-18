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
