#!/usr/bin/env python3
"""Build a PhpStorm UI theme plugin: Islands Dark recolored with Omarchy's Tokyo Night palette.

Usage: ui_theme.py <ManyIslandsDark.theme.json> <editor-scheme.icls> <out.jar> <since-build>

Islands Dark is copied from the installed IDE (lib/intellij.platform.resources.jar), so the
layout tracks JetBrains' updates; only its colors are swapped.
"""
import json
import re
import sys
import zipfile

THEME_NAME = "Tokyo Night (Omarchy)"
THEME_ID = "omarchy-tokyo-night"
SCHEME_RES = "/colors/TokyoNightOmarchy.xml"

BG = "1a1b26"

# Neutral ramp: Tokyo Night blue-greys, matched step-for-step to Islands' gray-10..160 roles
GRAY = {
    10: "1a1b26", 20: "1f2335", 30: "24283b", 40: "292e42", 50: "3b4261", 60: "414868",
    70: "4c5375", 80: "565f89", 90: "6b7299", 100: "787fa8", 110: "8b93be", 120: "9aa5ce",
    130: "a9b1d6", 140: "c0caf5", 150: "d0d7f7", 160: "e5e9fb",
}
# Extra darker neutrals (Omarchy dark/darker backgrounds) for literal greys below gray-10
DEEP = ["16161e", "13141c", "0e0e14"]

HUES = {
    "blue": "7aa2f7", "green": "9ece6a", "red": "f7768e", "yellow": "e0af68",
    "orange": "ff9e64", "purple": "bb9af7", "teal": "73daca",
}


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexc(c):
    return "".join(f"{max(0, min(255, round(x))):02x}" for x in c)


def mix(a, b, t):
    a, b = rgb(a), rgb(b)
    return hexc(tuple(x + (y - x) * t for x, y in zip(a, b)))


def lum(h):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b



def build_ramp(anchor, orig):
    """Recreate a 10..160 ramp in a Tokyo Night hue, keeping Islands' saturation/lightness per
    step (so buttons, badges and banners keep the same contrast and vibrancy)."""
    import colorsys
    ah = colorsys.rgb_to_hls(*(x / 255 for x in rgb(anchor)))[0]
    out = {}
    for step, ohex in orig.items():
        _, l, s = colorsys.rgb_to_hls(*(x / 255 for x in rgb(ohex)))
        out[step] = hexc(tuple(x * 255 for x in colorsys.hls_to_rgb(ah, l, s)))
    return out


def is_neutral(h):
    r, g, b = rgb(h)
    return max(r, g, b) - min(r, g, b) <= 14


NEUTRALS = list(GRAY.values()) + DEEP


def remap_literal(v):
    """Map a literal neutral grey (with optional alpha) to the nearest Tokyo Night neutral."""
    m = re.fullmatch(r"#([0-9A-Fa-f]{6})([0-9A-Fa-f]{2})?", v)
    if not m:
        return v
    h, alpha = m.group(1).lower(), m.group(2) or ""
    if h in ("000000", "ffffff") or not is_neutral(h):
        return v
    best = min(NEUTRALS, key=lambda n: abs(lum(n) ** 0.5 - lum(h) ** 0.5))
    return "#" + best + alpha


def walk(o):
    if isinstance(o, dict):
        return {k: walk(v) for k, v in o.items()}
    if isinstance(o, list):
        return [walk(v) for v in o]
    if isinstance(o, str) and o.startswith("#"):
        return remap_literal(o)
    return o


def main(src, icls, out, since_build):
    theme = json.load(open(src))
    colors = theme["colors"]

    # 1. Neutral ramp
    for step, v in GRAY.items():
        colors[f"gray-{step}"] = "#" + v
    # 2. Hue ramps, luminance-matched to the originals
    for hue, anchor in HUES.items():
        orig = {int(k.split("-")[1]): colors[k].lstrip("#")[:6]
                for k in colors if re.fullmatch(rf"{hue}-\d+", k)}
        for step, v in build_ramp(anchor, orig).items():
            colors[f"{hue}-{step}"] = "#" + v

    # 3. Non-ramp literals
    colors.update({
        "transparent": f"#{BG}00",
        "editor-text": "#c0caf5",
        "search-match-bg": "#e0af68",
        "tab-file-color-mask-bg": f"#{BG}80",
        "popup-completion-match-text": "#7aa2f7",
        "text-link": "#7aa2f7",
        "got-it-text-link": "#7dcfff",
    })

    ui = walk(theme["ui"])  # remap stray literal greys in the ui section
    # File colors (project tree tints, e.g. tests / library roots) in Tokyo Night hues
    ui["FileColor"] = {
        "Yellow": "#" + mix(BG, "e0af68", 0.10),
        "Green": "#" + mix(BG, "9ece6a", 0.09),
        "Orange": "#" + mix(BG, "ff9e64", 0.13),
        "Rose": "#" + mix(BG, "f7768e", 0.14),
        "Violet": "#" + mix(BG, "bb9af7", 0.14),
        "Blue": "#" + mix(BG, "7aa2f7", 0.12),
        "Gray": "#292e42",
    }
    dbg = ui.setdefault("Debugger", {}).setdefault("Variables", {})
    dbg.update({"valueForeground": "#ff9e64", "changedValueForeground": "#7aa2f7",
                "modifyingValueForeground": "#7aa2f7", "typeForeground": "#565f89",
                "collectingDataForeground": "#565f89",
                "evaluatingExpressionForeground": "#565f89"})
    ui["MemoryIndicator"] = {**ui.get("MemoryIndicator", {}), "usedBackground": "#3d59a180"}
    git = ui.setdefault("VersionControl", {}).setdefault("GitLog", {})
    git.update({"headIconColor": "#e0af68", "localBranchIconColor": "#9ece6a",
                "remoteBranchIconColor": "#bb9af7"})

    theme.update({
        "name": THEME_NAME,
        "author": "Omarchy Tokyo Night (based on JetBrains Islands Dark)",
        "editorScheme": SCHEME_RES,
        "colors": colors,
        "ui": ui,
    })
    theme["icons"] = {"ColorPalette": {"#CED0D6": "icon-default-stroke"}}

    plugin_xml = f"""<idea-plugin>
  <id>local.omarchy.tokyo-night</id>
  <name>{THEME_NAME}</name>
  <version>1.0.0</version>
  <vendor>local</vendor>
  <description>Islands Dark UI theme + editor scheme in Omarchy's Tokyo Night palette.</description>
  <idea-version since-build="{since_build}"/>
  <depends>com.intellij.modules.platform</depends>
  <extensions defaultExtensionNs="com.intellij">
    <themeProvider id="{THEME_ID}" path="/themes/TokyoNightOmarchy.theme.json" targetUi="islands"/>
  </extensions>
</idea-plugin>
"""
    entries = {
        "META-INF/plugin.xml": plugin_xml,
        "themes/TokyoNightOmarchy.theme.json": json.dumps(theme, indent=2),
        SCHEME_RES.lstrip("/"): open(icls).read(),
    }
    # Fixed timestamps, so an unchanged rebuild gives a byte-identical jar.
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in entries.items():
            z.writestr(zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0)), data,
                       compress_type=zipfile.ZIP_DEFLATED)


if __name__ == "__main__":
    main(*sys.argv[1:5])
