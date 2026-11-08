#!/usr/bin/env bash
# Build the Tokyo Night (Omarchy) theme plugin for PhpStorm and install it.
# The UI theme is the installed IDE's Islands Dark recolored, plus a matching
# editor scheme. Rerun after a PhpStorm update to rebuild against it.
# Skips if PhpStorm isn't installed. `--uninstall` removes the plugin.
set -euo pipefail
shopt -s nullglob

repo=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
src="$repo/setup/phpstorm-tokyo-night"
plugin=tokyo-night-omarchy

# PhpStorm via Toolbox, or a system-wide install.
ide=""
for dir in "$HOME/.local/share/JetBrains/Toolbox/apps/phpstorm" /opt/phpstorm* /usr/share/phpstorm*; do
  if [[ -f $dir/product-info.json ]]; then
    ide=$dir
    break
  fi
done

if [[ -z $ide ]]; then
  echo "Skipped: PhpStorm isn't installed."
  exit 0
fi

product() {
  python3 -I -c 'import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])' \
    "$ide/product-info.json" "$1"
}

data_dir=$(product dataDirectoryName) # e.g. PhpStorm2026.3
build=$(product buildNumber)          # e.g. 263.7307.215
dest="$HOME/.local/share/JetBrains/$data_dir/$plugin"

if [[ ${1:-} == "--uninstall" ]]; then
  rm -rf "$dest"
  echo "Removed $dest. Restart PhpStorm and pick another theme."
  exit 0
fi

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

python3 -I - "$ide/lib/intellij.platform.resources.jar" "$tmp/islands.json" <<'EOF'
import sys, zipfile
with zipfile.ZipFile(sys.argv[1]) as z, open(sys.argv[2], "wb") as out:
    out.write(z.read("themes/islands/ManyIslandsDark.theme.json"))
EOF

python3 -I "$src/editor_scheme.py" "$tmp/scheme.icls"
python3 -I "$src/ui_theme.py" "$tmp/islands.json" "$tmp/scheme.icls" "$tmp/$plugin.jar" "${build%%.*}"

if cmp -s "$tmp/$plugin.jar" "$dest/lib/$plugin.jar"; then
  echo "Already up to date: $dest"
  exit 0
fi

install -Dm644 "$tmp/$plugin.jar" "$dest/lib/$plugin.jar"
echo "Installed into $dest."
echo "Restart PhpStorm, then pick Tokyo Night (Omarchy) under Settings > Appearance > Theme."
