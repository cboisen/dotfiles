# Hyprland workflow

- `~/.config/hypr/scripts/launch-workflow.sh` opens browser, terminal,
  PhpStorm and Slack on workspaces 1, 2, 3 and 5.
- `~/.config/hypr/scripts/setup-{laptop,home,aarhus,holstebro}.sh` write the
  workspace-to-monitor rules to `~/.config/hypr/workspaces.lua`, apply the
  matching hyprmon profile and reload Hyprland.
- `~/.config/hyprmon/profiles/` holds those hyprmon profiles. Home has the
  27GL850 at 2560x1440@120 with VRR off to stop it flickering; keep that if you
  re-save it.
- `~/.config/hypr/bindings.lua` binds the scripts to keys, plus my other
  binding overrides.

## Setup

```bash
cd ~/Code/dotfiles
stow hypr-workflow
```

## If a link turns into a file

hyprmon (when saving a profile) and Omarchy migrations (when editing
`bindings.lua`) may replace a link with a regular file. The repo then stops
seeing changes. Pull the file back in and check what changed:

```bash
cd ~/Code/dotfiles
stow --adopt hypr-workflow
git diff
```
