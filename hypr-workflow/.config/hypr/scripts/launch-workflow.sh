#!/bin/bash
# Launch daily workflow apps on their designated workspaces

hyprctl dispatch 'hl.dsp.exec_cmd("[workspace 1 silent] uwsm-app -- omarchy-launch-browser")'
hyprctl dispatch 'hl.dsp.exec_cmd("[workspace 2 silent] uwsm-app -- xdg-terminal-exec")'
hyprctl dispatch 'hl.dsp.exec_cmd("[workspace 3 silent] uwsm-app -- phpstorm")'
hyprctl dispatch 'hl.dsp.exec_cmd("[workspace 5 silent] uwsm-app -- slack")'
