# Omarchy global workspaces

Makes `Super + 1–0` the same workspaces on every monitor again, undoing
[omacom/omarchy#15655](https://github.com/omacom/omarchy/pull/15655).

## Setup

```bash
cd ~/Code/dotfiles
stow omarchy-global-workspaces
./setup/omarchy-global-workspaces.sh
```

## Uninstall

```bash
cd ~/Code/dotfiles
./setup/omarchy-global-workspaces.sh --uninstall
stow -D omarchy-global-workspaces
```
