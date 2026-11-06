#!/bin/bash
# Clear workspace-to-monitor assignments (laptop uses all workspaces on built-in display)
cat > ~/.config/hypr/workspaces.lua << 'EOF'
-- Dynamic workspace-to-monitor assignments
-- This file is written by the setup-*.sh scripts in ~/.config/hypr/scripts/
-- Do not edit manually — changes will be overwritten on next profile switch
EOF

hyprmon --profile Laptop
hyprctl reload
