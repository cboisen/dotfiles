-- Keep only your personal keybinding overrides here. Add new bindings or
-- unbind defaults before replacing them.

-- See current bindings and descriptions:
--   omarchy menu keybindings --print

-- To disable every Omarchy default binding, set this in
-- ~/.config/hypr/hyprland.lua before require("default.hypr.omarchy"), then add
-- only the bindings you want below:
--   omarchy_default_bindings = false

-- To disable all preinstalled app/webapp bindings, set:
--   omarchy_preinstalled_bindings = false

-- Add a new binding.
-- o.bind("SUPER + SHIFT + R", "SSH", "alacritty -e ssh your-server")

-- Change an existing binding by unbinding it first, then binding the key again.
-- This example changes SUPER+SPACE from the launcher to the Omarchy root menu.
-- hl.unbind("SUPER + SPACE")
-- o.bind("SUPER + SPACE", "Omarchy menu", "omarchy-menu toggle root")

-- Disable a default binding without replacing it.
-- hl.unbind("SUPER + SHIFT + B")

-- Logitech MX Keys examples:
-- o.bind("SUPER + SHIFT + S", nil, "omarchy-capture-screenshot")
-- o.bind("SUPER + H", nil, "voxtype record toggle")
-- o.bind("SUPER + PERIOD", nil, "omarchy-shell shell toggle omarchy.emojis")

-- Launch daily workflow apps on their designated workspaces.
o.bind("SUPER + CTRL + aring", "Launch workflow apps", "~/.config/hypr/scripts/launch-workflow.sh")

-- Monitor setup profiles (each script writes hypr/workspaces.lua, then applies
-- the matching hyprmon profile). See ~/.config/hypr/scripts/.
o.bind("SUPER + SHIFT + L", "Laptop only", "~/.config/hypr/scripts/setup-laptop.sh")
o.bind("SUPER + SHIFT + H", "Holstebro office", "~/.config/hypr/scripts/setup-holstebro.sh")
o.bind("SUPER + SHIFT + K", "Aarhus office", "~/.config/hypr/scripts/setup-aarhus.sh")
o.bind("SUPER + SHIFT + J", "Home", "~/.config/hypr/scripts/setup-home.sh")

-- Unbinds
hl.unbind("CTRL + ALT + J")

-- Rebind SUPER+SHIFT+S to take a screenshot
hl.unbind("SUPER + SHIFT + S")
o.bind("SUPER + SHIFT + S", "Screenshot", "omarchy-capture-screenshot")

-- Rebind SUPER+SHIFT+C from HEY Calendar to Google Calendar
hl.unbind("SUPER + SHIFT + C")
o.bind("SUPER + SHIFT + C", "Google Calendar", { webapp = "https://calendar.google.com" })

-- Mute on the keyboard home row, for keyboards without media keys.
o.bind("SUPER + CTRL + M", "Mute", "omarchy-audio-output-volume mute-toggle", { locked = true })
