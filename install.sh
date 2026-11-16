#!/usr/bin/env bash
# Stow every package, then run the setup/ scripts. Files in ~ that block a
# package are moved to <file>.bak.<timestamp>. Safe to rerun.
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

# Paths (relative to ~) a dry run reports as conflicts.
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
  echo "Backed up (diff, then delete):"
  printf '  %s\n' "${backups[@]}"
fi

echo "All installed."
