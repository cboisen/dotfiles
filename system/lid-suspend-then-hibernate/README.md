# Lid: suspend-then-hibernate

Closing the laptop lid suspends, then hibernates after 2 hours (or sooner if
the battery runs low), instead of staying suspended until the battery dies.

With an external display connected, closing the lid still does nothing
(clamshell mode).

If hibernation isn't set up yet, the setup script offers to run `omarchy
hibernation setup` (a swapfile the size of your RAM, plus a reboot). Say no and
the lid keeps doing plain suspend.

Change the delay in `etc/systemd/sleep.conf.d/30-hibernate-delay.conf`.

These files go in `/etc`, so they are copied into place by a setup script
rather than stowed.

## Setup

```bash
cd ~/Code/dotfiles
./setup/lid-suspend-then-hibernate.sh
```

Run it again after editing the files here.

## Uninstall

```bash
cd ~/Code/dotfiles
./setup/lid-suspend-then-hibernate.sh --uninstall
```
