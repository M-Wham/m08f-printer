# m08f-printer — AUR Release Runbook

Step-by-step, copy-paste guide to finish the AUR work: merge the branch, optionally
smoke-test the package, set up your AUR account, publish, and verify it's live.

Run everything from the repo unless noted:

```bash
cd ~/Projects/thermal-printer
```

---

## Where things stand

- Branch `aur-package` holds the finished `packaging/aur/` (PKGBUILD, .SRCINFO,
  .gitignore, PUBLISHING.md) plus the design/plan docs.
- The PKGBUILD already builds a verified package
  (`m08f-printer-0.1.0-1-any.pkg.tar.zst`); checksum pins the real `v0.1.0`
  GitHub tarball.
- Tag `v0.1.0` is pushed; URL fix is on `main`.
- Nothing is on the AUR yet.

---

## Step 1 — Merge the branch into main

```bash
cd ~/Projects/thermal-printer
git checkout main
git merge --ff-only aur-package
git push origin main
```

Then delete the now-merged feature branch:

```bash
git branch -d aur-package
```

Confirm:

```bash
git log --oneline -4
git status
```

Expect a clean tree and the AUR commit at the top of `main`.

---

## Step 2 — (Optional) Smoke-test the package locally

Install the package you built, confirm the CLI works, then remove it. This pulls
the runtime deps (`python-pyserial`, `python-pillow`, `ghostscript`, `cups`).

```bash
sudo pacman -U packaging/aur/m08f-printer-0.1.0-1-any.pkg.tar.zst
```

> If that `.zst` no longer exists (e.g. fresh checkout), rebuild it first:
> `cd packaging/aur && makepkg -f && cd ../..`

Check it installed and runs:

```bash
which m08f
m08f status
pacman -Ql m08f-printer | grep -E "cups/backend|udev|model/m08f.ppd"
```

Remove it again (we only wanted to verify):

```bash
sudo pacman -R m08f-printer
```

---

## Step 3 — Set up your AUR account (one-time)

> ⛔ **BLOCKED as of 2026-06-18:** AUR account registration is currently disabled
> ("Account registration is currently disabled"). Steps 3–4 are on hold until it's
> re-enabled. Everything else (package built, tested, merged, tag pushed) is done.

Skip if you already have an AUR account with your SSH key registered.

1. Create an account at https://aur.archlinux.org (Register).

2. You already have an SSH key (`~/.ssh/id_ed25519`). Print the **public** key:

   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

   (No key yet? Make one: `ssh-keygen -t ed25519 -C "aur"` then print the `.pub`.)

3. On aur.archlinux.org: **My Account → SSH Public Key** → paste the full line →
   **Update**.

4. Test the connection (you'll be asked for your key passphrase):

   ```bash
   ssh aur@aur.archlinux.org help
   ```

   A help/usage message means auth works. "Permission denied (publickey)" means the
   key isn't registered correctly — recheck step 3.

---

## Step 4 — Publish to the AUR

The AUR repo is created automatically on your first `git push`.

```bash
cd ~/Projects
git clone ssh://aur@aur.archlinux.org/m08f-printer.git aur-m08f-printer
cp thermal-printer/packaging/aur/PKGBUILD thermal-printer/packaging/aur/.SRCINFO aur-m08f-printer/
cd aur-m08f-printer
makepkg --printsrcinfo > .SRCINFO   # regenerate in place, just to be safe
git add PKGBUILD .SRCINFO
git commit -m "Initial upload: m08f-printer 0.1.0"
git push
```

---

## Step 5 — Verify it's live

```bash
# Web page should now exist:
xdg-open https://aur.archlinux.org/packages/m08f-printer

# Or install it the way users will (needs an AUR helper like yay):
yay -S m08f-printer
```

---

## Future releases (when you cut a new version)

```bash
cd ~/Projects/thermal-printer

# 1. Bump version in pyproject.toml, commit, then tag + push:
#    (edit pyproject.toml version = "X.Y.Z" first)
git tag vX.Y.Z && git push origin vX.Y.Z

# 2. Update the PKGBUILD:
#    - set pkgver=X.Y.Z and pkgrel=1
cd packaging/aur
makepkg -g          # prints the new sha256sums line; paste it into PKGBUILD
makepkg -f          # rebuild to confirm it still packages
makepkg --printsrcinfo > .SRCINFO
cd ../..
git add packaging/aur/PKGBUILD packaging/aur/.SRCINFO
git commit -m "release: vX.Y.Z" && git push

# 3. Copy PKGBUILD + .SRCINFO into the AUR clone, commit, push (as in Step 4).
```

---

## Troubleshooting

- `git merge --ff-only` fails — `main` and the branch diverged; use
  `git merge aur-package` (a merge commit) instead.
- `makepkg` "missing dependencies" — install build deps:
  `sudo pacman -S --needed --asdeps python-build python-installer python-wheel python-setuptools`.
- AUR push "Permission denied (publickey)" — SSH key not registered; redo Step 3.
- AUR rejects push "missing .SRCINFO" — you forgot `makepkg --printsrcinfo > .SRCINFO`.
