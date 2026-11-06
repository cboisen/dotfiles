# dotfiles

Managed with [GNU Stow](https://www.gnu.org/software/stow/). Each top-level
folder except `setup/` and `system/` is a package.

`system/` holds `/etc` config, which the setup scripts copy into place.

## New machine

```bash
omarchy pkg add stow
git clone https://github.com/cboisen/dotfiles.git ~/Code/dotfiles
cd ~/Code/dotfiles
./install.sh
```

`install.sh` stows every package, then runs each script in `setup/`.
