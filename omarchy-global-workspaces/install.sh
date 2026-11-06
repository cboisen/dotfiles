#!/usr/bin/env bash
# Restore Omarchy's global workspaces (undo omacom/omarchy#15655).
#
# - Symlinks hypr/global-workspaces.lua into ~/.config/hypr and requires it
#   from hyprland.lua, right after require("hypr.bindings").
# - Symlinks the patched bar widget into ~/.config/omarchy/plugins and swaps
#   omarchy.workspaces for it in ~/.config/omarchy/shell.json.
# - Reloads Hyprland and moves any workspace numbered 11+ back to 1-10.
#
# Safe to run more than once. Undo with ./install.sh --uninstall.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
hypr="$HOME/.config/hypr"
plugins="$HOME/.config/omarchy/plugins"
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

reload_hyprland() {
  if command -v hyprctl >/dev/null && hyprctl monitors >/dev/null 2>&1; then
    hyprctl reload >/dev/null
    sleep 1
    local errors
    errors=$(hyprctl configerrors)
    if [[ -n $errors && $errors != "ok" ]]; then
      echo "Hyprland config errors:" >&2
      echo "$errors" >&2
      exit 1
    fi
  fi
}

if [[ ${1:-} == "--uninstall" ]]; then
  rm -f "$hypr/global-workspaces.lua"
  if grep -qF 'require("hypr.global-workspaces")' "$hypr/hyprland.lua"; then
    backup "$hypr/hyprland.lua"
    sed -i '/require("hypr.global-workspaces")/d' "$hypr/hyprland.lua"
  fi
  swap_widget "$plugin_id" "omarchy.workspaces"
  rm -rf "${plugins:?}/$plugin_id"
  reload_hyprland
  echo "Uninstalled. Omarchy's per-monitor workspaces are back."
  exit 0
fi

# Hyprland override
mkdir -p "$hypr"
ln -sfn "$here/hypr/global-workspaces.lua" "$hypr/global-workspaces.lua"
if ! grep -qF 'require("hypr.global-workspaces")' "$hypr/hyprland.lua"; then
  if ! grep -q '^require("hypr.bindings")' "$hypr/hyprland.lua"; then
    echo "Couldn't find require(\"hypr.bindings\") in $hypr/hyprland.lua; add this line after it yourself:" >&2
    echo "  $require_line" >&2
    exit 1
  fi
  backup "$hypr/hyprland.lua"
  sed -i "s|^require(\"hypr.bindings\")\$|&\n$require_line|" "$hypr/hyprland.lua"
fi

# Bar widget. The plugin folder is real and its files are symlinks, so the
# shell's plugin scanner sees an ordinary folder.
mkdir -p "$plugins/$plugin_id"
for file in manifest.json Workspaces.qml; do
  ln -sfn "$here/plugins/$plugin_id/$file" "$plugins/$plugin_id/$file"
done
swap_widget "omarchy.workspaces" "$plugin_id"

reload_hyprland

# Workspaces Omarchy already moved into per-monitor blocks (11-20, 21-30, ...)
# go back to their number within 1-10, when that number is free.
if command -v hyprctl >/dev/null && hyprctl monitors >/dev/null 2>&1; then
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

echo "Installed. Workspaces 1-10 are global again."
