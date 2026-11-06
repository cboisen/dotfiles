# dotfiles

Managed with [GNU Stow](https://www.gnu.org/software/stow/). Each top-level
folder except `setup/` is a package.

## New machine

```bash
omarchy pkg add stow
git clone https://github.com/cboisen/dotfiles.git ~/Code/dotfiles
cd ~/Code/dotfiles

stow omarchy-global-workspaces
./setup/omarchy-global-workspaces.sh
```

Run `stow` from the repo root so it picks up `.stowrc`. If a file already
exists, `stow --adopt <package>` pulls it into the repo; check `git diff`.
