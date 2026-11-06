#!/usr/bin/env bash
# Install everything in this repo: stow each package into ~, then run the
# scripts in setup/ for the parts Stow can't do (edits to files Omarchy also
# writes, and config in /etc that is copied into place with sudo).
#
# The repo always wins: a file in ~ that is in the way of a package (Omarchy's
# own bindings.lua, or a link hyprmon turned back into a file) is moved aside
# to <file>.bak.<timestamp> first, and listed at the end so you can diff it.
#
# Safe to run more than once: packages are restowed and every setup script is
# idempotent. Stops at the first failure.
set -euo pipefail
shopt -s nullglob

repo=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$repo" # so stow picks up .stowrc

if ! command -v stow >/dev/null; then
  echo "Stow isn't installed. Run: omarchy pkg add stow" >&2
  exit 1
fi

# Every top-level folder except setup/ and system/ is a Stow package.
packages=()
for dir in */; do
  dir=${dir%/}
  [[ $dir == setup || $dir == system ]] && continue
  packages+=("$dir")
done

# Paths (relative to ~) that would stop Stow: real files, and links Stow
# doesn't own. A dry run lists them; it exits non-zero when there are any.
conflicts() {
  { stow --no --restow "$1" 2>&1 || true; } | sed -n \
    -e 's/^  \* cannot stow .* over existing target \(.*\) since neither a link nor a directory.*$/\1/p' \
    -e 's/^  \* existing target is not owned by stow: \(.*\)$/\1/p'
}

stamp=$(date +%s)
backups=()

# All packages first: some setup scripts refuse to run until their files are linked.
for pkg in "${packages[@]}"; do
  echo "==> stow $pkg"
  while IFS= read -r path; do
    [[ -n $path ]] || continue
    mv -- "$HOME/$path" "$HOME/$path.bak.$stamp"
    backups+=("~/$path.bak.$stamp")
  done < <(conflicts "$pkg")
  stow --restow "$pkg"
done

for script in setup/*.sh; do
  echo "==> $script"
  "$script"
done

if (( ${#backups[@]} )); then
  echo
  echo "Moved aside to make room for the repo's version (compare, then delete):"
  printf '  %s\n' "${backups[@]}"
fi

echo "All installed."
