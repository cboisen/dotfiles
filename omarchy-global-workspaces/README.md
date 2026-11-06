# Omarchy global workspaces

Undoes [omacom/omarchy#15655](https://github.com/omacom/omarchy/pull/15655), which
gave every monitor its own workspaces 1–10. With this installed, `Super + 1–0`
means the same workspace on every monitor again, and workspace rules (like the
ones in `~/.config/hypr/workspaces.lua`) decide which monitor each one lives on.

## Install

```bash
git clone https://github.com/cboisen/dotfiles.git ~/dotfiles
~/dotfiles/omarchy-global-workspaces/install.sh
```

The installer symlinks the files below into `~/.config`, so keep the clone
where it is. It is safe to run again, and backs up anything it edits as
`*.bak.<timestamp>`.

Undo with `~/dotfiles/omarchy-global-workspaces/install.sh --uninstall`.

## What's in here

| File | Installed as | Does |
|------|--------------|------|
| `hypr/global-workspaces.lua` | `~/.config/hypr/global-workspaces.lua`, required from `hyprland.lua` after `require("hypr.bindings")` | Turns off Omarchy's per-monitor renumbering (`o.workspaces.reconcile`) and rebinds the workspace keys to plain Hyprland dispatchers |
| `plugins/christoffer.workspaces/` | `~/.config/omarchy/plugins/christoffer.workspaces/`, replacing `omarchy.workspaces` in `shell.json` | The bar's workspace widget, cloned from `omarchy.workspaces` and patched to show global workspaces 1–10 |

## Caveats

- `global-workspaces.lua` works by replacing `o.workspaces.reconcile`, so it relies on how
  Omarchy implements per-monitor workspaces. After an Omarchy update, check
  `hyprctl configerrors` and that `Super + 1` still behaves.
- The bar widget is a copy of Omarchy's widget as of 4.5.0, so it won't get upstream fixes.
- One difference from before the PR: each monitor's bar highlights the workspace
  that monitor is showing, not only the focused one.
