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
./install.sh
```

`install.sh` stows every package, then runs each script in `setup/`. It asks
for sudo only when something in `/etc` needs to change. Run it again after
pulling changes.

The repo always wins. A file in `~` that is in the way of a package (Omarchy's
own `bindings.lua`, or a link hyprmon turned back into a file) is moved aside
to `<file>.bak.<timestamp>`, and the script lists those backups at the end.
Diff each one against the linked file to keep anything you changed there, then
delete it.

To install a single package by hand, see its README. Run `stow` from the repo
root so it picks up `.stowrc`. If a file already exists, `stow --adopt
<package>` pulls it into the repo; check `git diff`.
