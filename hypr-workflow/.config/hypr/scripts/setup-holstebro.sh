#!/bin/bash
# Write Holstebro workspace-to-monitor assignments, then apply monitor profile
cat > ~/.config/hypr/workspaces.lua << 'EOF'
-- Dynamic workspace-to-monitor assignments
-- This file is written by the setup-*.sh scripts in ~/.config/hypr/scripts/
-- Do not edit manually — changes will be overwritten on next profile switch

hl.workspace_rule({ workspace = "1", monitor = "desc:Dell Inc. DELL U2715H GH85D6C11P4S", default = true })
hl.workspace_rule({ workspace = "2", monitor = "desc:Dell Inc. DELL U2715H GH85D73B0Y6S", default = true })
hl.workspace_rule({ workspace = "3", monitor = "desc:Dell Inc. DELL U2715H GH85D6C11P4S" })
hl.workspace_rule({ workspace = "4", monitor = "desc:Dell Inc. DELL U2715H GH85D73B0Y6S" })
hl.workspace_rule({ workspace = "5", monitor = "desc:Dell Inc. DELL U2715H GH85D6C11P4S" })
hl.workspace_rule({ workspace = "6", monitor = "desc:Dell Inc. DELL U2715H GH85D73B0Y6S" })
hl.workspace_rule({ workspace = "7", monitor = "desc:Dell Inc. DELL U2715H GH85D6C11P4S" })
hl.workspace_rule({ workspace = "8", monitor = "desc:Dell Inc. DELL U2715H GH85D73B0Y6S" })
hl.workspace_rule({ workspace = "9", monitor = "desc:Dell Inc. DELL U2715H GH85D6C11P4S" })
EOF

hyprmon --profile Holstebro
hyprctl reload
