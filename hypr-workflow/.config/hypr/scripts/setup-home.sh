#!/bin/bash
# Write Home workspace-to-monitor assignments, then apply monitor profile
cat > ~/.config/hypr/workspaces.lua << 'EOF'
-- Dynamic workspace-to-monitor assignments
-- This file is written by the setup-*.sh scripts in ~/.config/hypr/scripts/
-- Do not edit manually — changes will be overwritten on next profile switch

hl.workspace_rule({ workspace = "1", monitor = "desc:LG Electronics 27GL850 007NTGY8L439", default = true })
hl.workspace_rule({ workspace = "2", monitor = "desc:LG Display 0x07C7", default = true })
hl.workspace_rule({ workspace = "3", monitor = "desc:LG Electronics 27GL850 007NTGY8L439" })
hl.workspace_rule({ workspace = "4", monitor = "desc:LG Display 0x07C7" })
hl.workspace_rule({ workspace = "5", monitor = "desc:LG Electronics 27GL850 007NTGY8L439" })
hl.workspace_rule({ workspace = "6", monitor = "desc:LG Display 0x07C7" })
hl.workspace_rule({ workspace = "7", monitor = "desc:LG Electronics 27GL850 007NTGY8L439" })
hl.workspace_rule({ workspace = "8", monitor = "desc:LG Display 0x07C7" })
hl.workspace_rule({ workspace = "9", monitor = "desc:LG Electronics 27GL850 007NTGY8L439" })
EOF

# The 27GL850 flicker workaround (144Hz+VRR -> 120Hz/no-VRR) now lives in the
# Home hyprmon profile itself (~/.config/hyprmon/profiles/Home.json), so hyprmon
# writes the correct mode directly — no post-apply sed needed.
# NOTE: if you re-save the Home profile from hyprmon's TUI, set the 27GL850 back
# to 2560x1440@120 with VRR off, or the flicker returns.
hyprmon --profile Home
hyprctl reload
