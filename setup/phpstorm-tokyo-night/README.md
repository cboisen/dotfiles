# PhpStorm: Tokyo Night (Omarchy)

A PhpStorm theme in Omarchy's Tokyo Night colors: the UI and the editor.

- **UI:** PhpStorm's own Islands Dark theme with its colors swapped. Greys
  become Tokyo Night's blue-greys; accents take Tokyo Night's hues at Islands'
  brightness, so buttons and selections keep their contrast.
- **Editor:** the syntax colors of Omarchy's Neovim theme (`tokyonight-night`).
  Selecting the UI theme switches the editor scheme too.

```bash
./setup/phpstorm-tokyo-night.sh              # install, or rebuild after editing
./setup/phpstorm-tokyo-night.sh --uninstall
```

Then restart PhpStorm and pick **Tokyo Night (Omarchy)** under Settings >
Appearance > Theme (only needed the first time).

The plugin is built from the installed PhpStorm, so rerun the script after a
PhpStorm update. Colors live in `editor_scheme.py` and `ui_theme.py`.
