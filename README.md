# dotfiles

Managed with [GNU Stow](https://www.gnu.org/software/stow/). Each top-level
folder except `setup/` and `system/` is a package.

`system/` holds config that belongs outside `~` (in `/etc`). Its setup scripts
copy it into place with sudo instead of stowing it.

## New machine

```bash
omarchy pkg add stow
git clone https://github.com/cboisen/dotfiles.git ~/Code/dotfiles
cd ~/Code/dotfiles

stow omarchy-global-workspaces
./setup/omarchy-global-workspaces.sh

stow hypr-workflow

./setup/lid-suspend-then-hibernate.sh
```

Run `stow` from the repo root so it picks up `.stowrc`. If a file already
exists, `stow --adopt <package>` pulls it into the repo; check `git diff`.
