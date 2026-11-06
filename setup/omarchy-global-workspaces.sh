#!/usr/bin/env bash
# Wire up the stowed files for global workspaces (undo omacom/omarchy#15655).
#
# Run after `stow omarchy-global-workspaces`. Stow links the files; this does
# the two edits Stow can't, in files Omarchy also writes to:
#
# - requires hypr/global-workspaces.lua from ~/.config/hypr/hyprland.lua,
#   right after require("hypr.bindings")
# - swaps omarchy.workspaces for christoffer.workspaces in the bar
#   (~/.config/omarchy/shell.json)
#
# Then it reloads Hyprland and moves any workspace numbered 11+ back to 1-10.
#
# Safe to run more than once. `--uninstall` reverts the edits; run it before
# `stow -D omarchy-global-workspaces`.
set -euo pipefail

hypr="$HOME/.config/hypr"
shell_json="$HOME/.config/omarchy/shell.json"
plugin_id="christoffer.workspaces"
require_line='require("hypr.global-workspaces") -- undo per-monitor workspaces (omarchy#15655)'

backup() {
  [[ -f $1 ]] && cp "$1" "$1.bak.$(date +%s)"
}

swap_widget() {
  local from=$1 to=$2
  [[ -f $shell_json ]] || return 0
  grep -q "\"$from\"" "$shell_json" || return 0
  backup "$shell_json"
  local tmp
  tmp=$(mktemp)
  jq --arg from "$from" --arg to "$to" \
    '(.. | objects | select(.id? == $from) | .id) |= $to' "$shell_json" >"$tmp"
  mv "$tmp" "$shell_json"
}

hyprland_running() {
  command -v hyprctl >/dev/null && hyprctl monitors >/dev/null 2>&1
}

reload_hyprland() {
  hyprland_running || return 0
  hyprctl reload >/dev/null
  sleep 1
  local errors
  errors=$(hyprctl configerrors)
  if [[ -n $errors && $errors != "ok" ]]; then
    echo "Hyprland config errors:" >&2
    echo "$errors" >&2
    exit 1
  fi
}

if [[ ${1:-} == "--uninstall" ]]; then
  if grep -qF 'require("hypr.global-workspaces")' "$hypr/hyprland.lua"; then
    backup "$hypr/hyprland.lua"
    sed -i '/require("hypr.global-workspaces")/d' "$hypr/hyprland.lua"
  fi
  swap_widget "$plugin_id" "omarchy.workspaces"
  reload_hyprland
  echo "Edits reverted. Now run: stow -D omarchy-global-workspaces"
  exit 0
fi

# Refuse to wire things up before Stow has linked the files, or Hyprland would
# fail to load the missing module and the bar would lose its widget.
for file in "$hypr/global-workspaces.lua" "$HOME/.config/omarchy/plugins/$plugin_id/Workspaces.qml"; do
  if [[ ! -e $file ]]; then
    echo "Missing $file. Run \`stow omarchy-global-workspaces\` from the dotfiles repo first." >&2
    exit 1
  fi
done

if ! grep -qF 'require("hypr.global-workspaces")' "$hypr/hyprland.lua"; then
  if ! grep -q '^require("hypr.bindings")' "$hypr/hyprland.lua"; then
    echo "Couldn't find require(\"hypr.bindings\") in $hypr/hyprland.lua; add this line after it yourself:" >&2
    echo "  $require_line" >&2
    exit 1
  fi
  backup "$hypr/hyprland.lua"
  sed -i "s|^require(\"hypr.bindings\")\$|&\n$require_line|" "$hypr/hyprland.lua"
fi

swap_widget "omarchy.workspaces" "$plugin_id"

reload_hyprland

# Workspaces Omarchy already moved into per-monitor blocks (11-20, 21-30, ...)
# go back to their number within 1-10, when that number is free.
if hyprland_running; then
  ids=$(hyprctl workspaces -j | jq -r '.[] | select(.id > 0) | .id')
  for id in $ids; do
    (( id > 10 )) || continue
    target=$(( (id - 1) % 10 + 1 ))
    if ! grep -qx "$target" <<<"$ids"; then
      hyprctl dispatch "hl.dsp.workspace.change_id({ workspace = \"$id\", id = $target })" >/dev/null
      ids=$(printf '%s\n%s\n' "$ids" "$target")
      echo "Renumbered workspace $id -> $target"
    fi
  done
fi

echo "Done. Workspaces 1-10 are global again."
