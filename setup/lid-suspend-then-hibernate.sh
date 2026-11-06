#!/usr/bin/env bash
# Make closing the laptop lid suspend-then-hibernate instead of plain suspend.
#
# The config lives in /etc, outside Stow's reach (and logind runs with
# ProtectHome=yes, so it can't follow a symlink into $HOME anyway), so this
# copies the files from system/lid-suspend-then-hibernate/ into place and
# reloads logind. sudo is only needed when something actually changes.
#
# If hibernation isn't set up, it offers to run `omarchy hibernation setup`.
# Declined or unsupported: the lid keeps plain suspend, and any copy of these
# files left from before is removed, since logind can't act on
# suspend-then-hibernate without hibernation and would leave a closed laptop
# awake.
#
# Safe to run more than once. `--uninstall` removes the files again.
set -euo pipefail

repo=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
src="$repo/system/lid-suspend-then-hibernate"
files=(
  etc/systemd/logind.conf.d/30-lid-suspend-then-hibernate.conf
  etc/systemd/sleep.conf.d/30-hibernate-delay.conf
)

lid_action() {
  busctl get-property org.freedesktop.login1 /org/freedesktop/login1 \
    org.freedesktop.login1.Manager HandleLidSwitch | sed 's/^s "\(.*\)"$/\1/'
}

remove_installed() {
  local f removed=0
  for f in "${files[@]}"; do
    if [[ -e /$f ]]; then
      sudo rm -f "/$f"
      removed=1
    fi
  done
  if (( removed )); then
    sudo systemctl reload systemd-logind
  fi
}

if [[ ${1:-} == "--uninstall" ]]; then
  remove_installed
  echo "Removed. Closing the lid now does: $(lid_action)"
  exit 0
fi

if ! omarchy-hibernation-available; then
  ram=$(LC_ALL=C free --human | awk '/Mem/ {print $2}')
  if gum confirm "Hibernation isn't set up. Set it up now? It uses $ram of disk for swap."; then
    omarchy-hibernation-setup --force
  fi
fi

if ! omarchy-hibernation-available; then
  remove_installed
  echo "Skipped: hibernation isn't available, so closing the lid keeps doing plain suspend."
  exit 0
fi

# Freshly set up: the kernel only learns where to resume from at the next boot.
# Hibernating before then would boot fresh and lose the session.
if ! grep -q 'resume=' /proc/cmdline; then
  echo "Hibernation is set up but needs a reboot. Reboot, then run this again to finish." >&2
  exit 0
fi

changed=0
for f in "${files[@]}"; do
  if ! cmp -s "$src/$f" "/$f"; then
    sudo install -Dm644 -o root -g root "$src/$f" "/$f"
    changed=1
  fi
done

# logind rereads its config on reload; sleep.conf is read at each sleep.
if (( changed )); then
  sudo systemctl reload systemd-logind
fi

action=$(lid_action)
if [[ $action != "suspend-then-hibernate" ]]; then
  echo "logind still reports HandleLidSwitch=$action. Check /etc/systemd/logind.conf.d/." >&2
  exit 1
fi

if (( changed )); then
  echo "Done. Closing the lid now does: $action"
else
  echo "Already up to date. Closing the lid does: $action"
fi
