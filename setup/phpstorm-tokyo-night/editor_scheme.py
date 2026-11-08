#!/usr/bin/env python3
"""Generate a PhpStorm/IntelliJ editor color scheme from Omarchy's Tokyo Night palette
(mirrors tokyonight.nvim "night", which Omarchy's Neovim uses).

Usage: editor_scheme.py <out.icls>"""
import sys
from xml.sax.saxutils import quoteattr

# --- palette (Omarchy colors.toml + tokyonight-night extras) ---
bg = "1a1b26"
bg_dark = "16161e"
bg_highlight = "292e42"      # omarchy selection
lighter_bg = "24283b"
terminal_black = "414868"    # omarchy muted
fg = "c0caf5"                # bright_foreground
fg_dark = "a9b1d6"           # foreground
fg_gutter = "3b4261"
dark3 = "545c7e"
comment = "565f89"           # dark_foreground
dark5 = "737aa2"
blue0 = "3d59a1"
blue = "7aa2f7"
cyan = "7dcfff"
blue1 = "2ac3de"
blue2 = "0db9d7"
blue5 = "89ddff"
blue6 = "b4f9f8"
blue7 = "394b70"
magenta = "bb9af7"
magenta2 = "ff007c"
purple = "9d7cd8"
orange = "ff9e64"
yellow = "e0af68"
green = "9ece6a"
green1 = "73daca"
green2 = "41a6b5"
teal = "1abc9c"
red = "f7768e"
red1 = "db4b4b"
git_add = "449dab"
git_change = "6183bb"
git_delete = "914c54"
punct = "9abdf5"

BOLD, ITALIC, BOLD_ITALIC = 1, 2, 3

colors = {
    "CARET_COLOR": fg,
    "CARET_ROW_COLOR": "1f2335",
    "CONSOLE_BACKGROUND_KEY": bg,
    "GUTTER_BACKGROUND": bg,
    "LINE_NUMBERS_COLOR": fg_gutter,
    "LINE_NUMBER_ON_CARET_ROW_COLOR": "737aa2",
    "INDENT_GUIDE": "292e42",
    "SELECTED_INDENT_GUIDE": "3b4261",
    "SOFT_WRAP_SIGN_COLOR": fg_gutter,
    "WHITESPACES": "3b4261",
    "TEARLINE_COLOR": "292e42",
    "SELECTED_TEARLINE_COLOR": blue0,
    "RIGHT_MARGIN_COLOR": "292e42",
    "VISUAL_INDENT_GUIDE": "292e42",
    "METHOD_SEPARATORS_COLOR": "292e42",
    "SELECTION_BACKGROUND": "283457",
    "SELECTION_FOREGROUND": "",
    "DOCUMENTATION_COLOR": bg_dark,
    "LOOKUP_COLOR": bg_dark,
    "INFORMATION_HINT": bg_dark,
    "QUESTION_HINT": bg_dark,
    "ERROR_HINT": "2d202a",
    "NOTIFICATION_BACKGROUND": bg_dark,
    "FOLDED_TEXT_BORDER_COLOR": "3b4261",
    "ANNOTATIONS_COLOR": dark5,
    "ANNOTATIONS_LAST_COMMIT_COLOR": fg_dark,
    "ADDED_LINES_COLOR": git_add,
    "MODIFIED_LINES_COLOR": git_change,
    "DELETED_LINES_COLOR": git_delete,
    "WHITESPACES_MODIFIED_LINES_COLOR": "3d4f5a",
    "IGNORED_ADDED_LINES_BORDER_COLOR": git_add,
    "IGNORED_MODIFIED_LINES_BORDER_COLOR": git_change,
    "IGNORED_DELETED_LINES_BORDER_COLOR": git_delete,
    "VCS_ANNOTATIONS_COLOR_1": "2b3046",
    "VCS_ANNOTATIONS_COLOR_2": "272b40",
    "VCS_ANNOTATIONS_COLOR_3": "23263a",
    "VCS_ANNOTATIONS_COLOR_4": "1f2233",
    "VCS_ANNOTATIONS_COLOR_5": "1c1e2d",
    "DIFF_SEPARATORS_BACKGROUND": bg_dark,
    "FILESTATUS_ADDED": green,
    "FILESTATUS_MODIFIED": blue,
    "FILESTATUS_DELETED": red,
    "FILESTATUS_UNKNOWN": red,
    "FILESTATUS_IDEA_FILESTATUS_IGNORED": comment,
    "FILESTATUS_NOT_CHANGED_IMMEDIATE": blue,
    "FILESTATUS_NOT_CHANGED_RECURSIVE": blue,
    "FILESTATUS_MERGED": magenta,
    "FILESTATUS_addedOutside": green1,
    "FILESTATUS_modifiedOutside": cyan,
    "ScrollBar.Mac.Transparent.thumbColor": "3b426180",
    "ScrollBar.Mac.thumbColor": "3b426180",
    "ScrollBar.thumbColor": "3b426180",
    "ScrollBar.Transparent.thumbColor": "3b426180",
    "ScrollBar.hoverThumbColor": "545c7ecc",
    "ScrollBar.Transparent.hoverThumbColor": "545c7ecc",
    "BREADCRUMBS_CURRENT": "",
    "TAB_UNDERLINE": blue,
    "CONSOLE_RANGE_TO_EXECUTE": blue0,
}

attrs = {}


def a(key, fg=None, bg=None, style=None, effect=None, effect_type=None, error_stripe=None,
      base=None):
    attrs[key] = dict(fg=fg, bg=bg, style=style, effect=effect, effect_type=effect_type,
                      stripe=error_stripe, base=base)


# --- Text / general ---
a("TEXT", fg, bg)
a("DEFAULT_IDENTIFIER", fg)
a("IDENTIFIER_UNDER_CARET_ATTRIBUTES", bg="2e3c64", error_stripe=blue0)
a("WRITE_IDENTIFIER_UNDER_CARET_ATTRIBUTES", bg="3b3256", error_stripe=purple)
a("TEXT_SEARCH_RESULT_ATTRIBUTES", fg=bg, bg=orange, error_stripe=orange)
a("SEARCH_RESULT_ATTRIBUTES", bg="3d59a1", error_stripe=blue0)
a("WRITE_SEARCH_RESULT_ATTRIBUTES", bg="3d59a1", error_stripe=blue0)
a("MATCHED_BRACE_ATTRIBUTES", fg=orange, bg="3b4261", style=BOLD)
a("UNMATCHED_BRACE_ATTRIBUTES", fg=red, bg="3d2531")
a("FOLDED_TEXT_ATTRIBUTES", fg=dark5, bg="292e42")
a("HYPERLINK_ATTRIBUTES", fg=cyan, effect=cyan, effect_type=1)
a("FOLLOWED_HYPERLINK_ATTRIBUTES", fg=magenta, effect=magenta, effect_type=1)
a("CTRL_CLICKABLE", fg=cyan, effect=cyan, effect_type=1)
a("TODO_DEFAULT_ATTRIBUTES", fg=yellow, style=BOLD_ITALIC, error_stripe=yellow)
a("BOOKMARKS_ATTRIBUTES", error_stripe=orange)
a("BREAKPOINT_ATTRIBUTES", bg="3d2531", error_stripe=red)
a("EXECUTIONPOINT_ATTRIBUTES", bg="2e3c64", error_stripe=blue)
a("NOT_TOP_FRAME_ATTRIBUTES", bg="292e42")
a("LIVE_TEMPLATE_ATTRIBUTES", effect=blue, effect_type=0)
a("LIVE_TEMPLATE_INACTIVE_SEGMENT", fg=dark5)
a("INJECTED_LANGUAGE_FRAGMENT", bg="1e2030")
a("TEMPLATE_LANGUAGE_COLOR", bg="1e2030")
a("INLINE_PARAMETER_HINT", fg=dark5, bg="1f2335")
a("INLINE_PARAMETER_HINT_CURRENT", fg=fg, bg="2e3c64")
a("INLINE_PARAMETER_HINT_HIGHLIGHTED", fg=fg_dark, bg="292e42")
a("INLAY_DEFAULT", fg=dark5, bg="1f2335")
a("INLAY_TEXT_WITHOUT_BACKGROUND", fg=dark3)
a("BLOCK_TERMINAL_DEFAULT", fg=fg, bg=bg)
a("DELETED_TEXT_ATTRIBUTES", fg=comment, effect=comment, effect_type=3)
a("DUPLICATE_FROM_SERVER", bg="292e42")
a("INFO_ATTRIBUTES", effect=blue1, effect_type=2)
a("TYPO", effect=dark3, effect_type=2)
a("TEXT_STYLE_SUGGESTION", effect=dark3, effect_type=2)
a("GRAMMAR_ERROR", effect=green2, effect_type=2)

# --- Errors & inspections ---
a("ERRORS_ATTRIBUTES", effect=red1, effect_type=2, error_stripe=red1)
a("WRONG_REFERENCES_ATTRIBUTES", fg=red, error_stripe=red1)
a("BAD_CHARACTER", fg=red, effect=red1, effect_type=2)
a("WARNING_ATTRIBUTES", bg="2d2a2a", effect=yellow, effect_type=2, error_stripe=yellow)
a("GENERIC_SERVER_ERROR_OR_WARNING", effect=orange, effect_type=2, error_stripe=orange)
a("RUNTIME_ERROR", effect=red1, effect_type=2, error_stripe=red1)
a("WEAK_WARNING_ATTRIBUTES", effect=dark3, effect_type=2)
a("NOT_USED_ELEMENT_ATTRIBUTES", fg=dark5)
a("DEPRECATED_ATTRIBUTES", effect=dark5, effect_type=3)
a("MARKED_FOR_REMOVAL_ATTRIBUTES", effect=red, effect_type=3)

# --- Language defaults (inherited by most languages) ---
a("DEFAULT_KEYWORD", magenta, style=ITALIC)
a("DEFAULT_STRING", green)
a("DEFAULT_VALID_STRING_ESCAPE", magenta)
a("DEFAULT_INVALID_STRING_ESCAPE", red, effect=red1, effect_type=2)
a("DEFAULT_NUMBER", orange)
a("DEFAULT_CONSTANT", orange)
a("DEFAULT_LINE_COMMENT", comment, style=ITALIC)
a("DEFAULT_BLOCK_COMMENT", comment, style=ITALIC)
a("DEFAULT_DOC_COMMENT", comment, style=ITALIC)
a("DEFAULT_DOC_COMMENT_TAG", purple, style=ITALIC)
a("DEFAULT_DOC_COMMENT_TAG_VALUE", blue1, style=ITALIC)
a("DEFAULT_DOC_MARKUP", dark5)
a("DEFAULT_OPERATION_SIGN", blue5)
a("DEFAULT_BRACES", punct)
a("DEFAULT_BRACKETS", punct)
a("DEFAULT_PARENTHS", punct)
a("DEFAULT_COMMA", punct)
a("DEFAULT_DOT", blue5)
a("DEFAULT_SEMICOLON", punct)
a("DEFAULT_LABEL", blue)
a("DEFAULT_METADATA", yellow)
a("DEFAULT_ENTITY", orange)
a("DEFAULT_PREDEFINED_SYMBOL", blue1)
a("DEFAULT_FUNCTION_DECLARATION", blue)
a("DEFAULT_FUNCTION_CALL", blue)
a("DEFAULT_STATIC_METHOD", blue, style=ITALIC)
a("DEFAULT_INSTANCE_METHOD", blue)
a("DEFAULT_CLASS_NAME", blue1)
a("DEFAULT_CLASS_REFERENCE", blue1)
a("DEFAULT_INTERFACE_NAME", blue1, style=ITALIC)
a("DEFAULT_LOCAL_VARIABLE", fg)
a("DEFAULT_REASSIGNED_LOCAL_VARIABLE", fg, effect=dark3, effect_type=1)
a("DEFAULT_GLOBAL_VARIABLE", red)
a("DEFAULT_PARAMETER", yellow)
a("DEFAULT_REASSIGNED_PARAMETER", yellow, effect=dark3, effect_type=1)
a("DEFAULT_INSTANCE_FIELD", green1)
a("DEFAULT_STATIC_FIELD", green1, style=ITALIC)
a("DEFAULT_HIGHLIGHTED_REFERENCE", fg=cyan, bg="292e42")
a("DEFAULT_TEMPLATE_LANGUAGE_COLOR", bg="1e2030")
a("DEFAULT_TAG", red)
a("DEFAULT_ATTRIBUTE", green1)
a("DEFAULT_DOC_COMMENT_TAG_VALUE", blue1)

# --- PHP ---
a("PHP_VAR", fg)
a("PHP_EXEC_COMMAND_ID", green)
a("PHP_SCRIPTING_BACKGROUND", bg=bg)
a("PHP_MARKUP_ID", red)
a("PHP_MAGIC_MEMBER_ACCESS", green1, style=ITALIC)
a("PHP_NAMED_ARGUMENT", yellow, style=ITALIC)
a("PHP_PARAMETER", yellow)
a("PHP_IDENTIFIER", fg)
a("PHP_HEREDOC_ID", magenta)
a("PHP_HEREDOC_CONTENT", green)
a("PHP_ESCAPE_SEQUENCE", magenta)
a("PHP_KEYWORD", magenta, style=ITALIC)
a("PHP_CONSTANT", orange)
a("PHP_NUMBER", orange)
a("PHP_STRING", green)
a("PHP_OPERATION_SIGN", blue5)
a("PHP_PREDEFINED SYMBOL", blue1)
a("PHP_CLASS", blue1)
a("PHP_INTERFACE", blue1, style=ITALIC)
a("PHP_FUNCTION_CALL", blue)
a("PHP_METHOD_CALL", blue)
a("PHP_STATIC_METHOD_CALL", blue, style=ITALIC)
a("PHP_FIELD", green1)
a("PHP_STATIC_FIELD", green1, style=ITALIC)
a("PHP_ATTRIBUTE", yellow)
a("PHP_ATTRIBUTE_NAME", yellow)
a("PHP_LIGHT_TYPE", blue1, style=ITALIC)
a("PHP_TYPE", blue1)
a("PHP_THIS", red, style=ITALIC)
a("PHP_DOC_TAG", purple, style=ITALIC)
a("PHP_DOC_PARAMETER", yellow, style=ITALIC)
a("PHP_DOC_COMMENT_ID", comment, style=ITALIC)
a("PHP_COMMENT", comment, style=ITALIC)
a("PHP_VAR_VAR", red)
a("PHP_TAG", red, style=BOLD)
a("PHP_ENUM_CASE", orange)

# --- Blade ---
a("BLADE_DIRECTIVE", magenta, style=ITALIC)
a("BLADE_ECHO", blue5)
a("BLADE_TEMPLATE_BACKGROUND", bg=bg)
a("BLADE_COMMENT", comment, style=ITALIC)
a("BLADE_PARENTHS", punct)

# --- HTML / XML ---
a("HTML_TAG", punct)
a("HTML_TAG_NAME", red)
a("HTML_CUSTOM_TAG_NAME", blue1)
a("HTML_ATTRIBUTE_NAME", green1, style=ITALIC)
a("HTML_ATTRIBUTE_VALUE", green)
a("HTML_ENTITY_REFERENCE", orange)
a("HTML_COMMENT", comment, style=ITALIC)
a("XML_TAG", punct)
a("XML_TAG_NAME", red)
a("XML_NS_PREFIX", magenta)
a("XML_ATTRIBUTE_NAME", green1, style=ITALIC)
a("XML_ATTRIBUTE_VALUE", green)
a("XML_ENTITY_REFERENCE", orange)
a("XML_PROLOGUE", dark5)
a("XML_TAG_DATA", fg)
a("HTML_CODE", fg)

# --- CSS / SCSS ---
a("CSS.TAG_NAME", red)
a("CSS.CLASS_NAME", green1)
a("CSS.IDENT", fg)
a("CSS.IDENTIFIER", fg)
a("CSS.ID_SELECTOR", orange)
a("CSS.PSEUDO", cyan)
a("CSS.PROPERTY_NAME", blue)
a("CSS.PROPERTY_VALUE", orange)
a("CSS.KEYWORD", magenta, style=ITALIC)
a("CSS.FUNCTION", blue1)
a("CSS.NUMBER", orange)
a("CSS.UNIT", orange)
a("CSS.COLOR", orange)
a("CSS.STRING", green)
a("CSS.URL", green, effect=green, effect_type=1)
a("CSS.IMPORTANT", red, style=BOLD)
a("CSS.ATTRIBUTE_NAME", green1)
a("CSS.HASH", orange)
a("CSS.COMMENT", comment, style=ITALIC)
a("SASS_VARIABLE", red)
a("SCSS_VARIABLE", red)
a("LESS_VARIABLE", red)
a("SASS_MIXIN", blue)

# --- JavaScript / TypeScript ---
a("JS.LOCAL_VARIABLE", fg)
a("JS.GLOBAL_VARIABLE", red)
a("JS.PARAMETER", yellow)
a("JS.INSTANCE_MEMBER_FUNCTION", blue)
a("JS.STATIC_MEMBER_FUNCTION", blue, style=ITALIC)
a("JS.GLOBAL_FUNCTION", blue)
a("JS.INSTANCE_MEMBER_VARIABLE", green1)
a("JS.STATIC_MEMBER_VARIABLE", green1, style=ITALIC)
a("JS.REGEXP", blue6)
a("JS.CLASS", blue1)
a("JS.DECORATOR", yellow)
a("JS.PRIMITIVE.TYPE", blue1, style=ITALIC)
a("TS.TYPE_PARAMETER", blue1, style=ITALIC)
a("TS.TYPE_GUARD", magenta)
a("TS.MODULE_NAME", blue1)
a("JS.INJECTED_LANGUAGE_FRAGMENT", bg="1e2030")

# --- Vue ---
a("VUE_INTERPOLATION_DELIMITER", blue5)

# --- JSON / YAML / TOML / .env / properties ---
a("JSON.PROPERTY_KEY", blue)
a("JSON.KEYWORD", orange)
a("JSON.NUMBER", orange)
a("JSON.STRING", green)
a("JSON.BRACES", punct)
a("JSON.BRACKETS", punct)
a("JSON.COLON", blue5)
a("JSON.COMMA", punct)
a("YAML_SCALAR_KEY", blue)
a("YAML_SCALAR_VALUE", green)
a("YAML_SCALAR_STRING", green)
a("YAML_SCALAR_DSTRING", green)
a("YAML_SCALAR_LIST", green)
a("YAML_TEXT", green)
a("YAML_ANCHOR", orange)
a("YAML_SIGN", blue5)
a("YAML_COMMENT", comment, style=ITALIC)
a("org.toml.KEY", blue)
a("org.toml.STRING", green)
a("DOTENV_KEY", blue)
a("DOTENV_VALUE", green)
a("PROPERTIES.KEY", blue)
a("PROPERTIES.VALUE", green)
a("PROPERTIES.KEY_VALUE_SEPARATOR", blue5)

# --- Markdown ---
for i, col in enumerate([blue, yellow, green, green1, magenta, purple], start=1):
    a(f"MARKDOWN_HEADER_LEVEL_{i}", col, style=BOLD)
a("MARKDOWN_BOLD", orange, style=BOLD)
a("MARKDOWN_ITALIC", magenta, style=ITALIC)
a("MARKDOWN_BOLDITALIC", orange, style=BOLD_ITALIC)
a("MARKDOWN_STRIKETHROUGH", dark5, effect=dark5, effect_type=3)
a("MARKDOWN_CODE_SPAN", green1, bg="1e2030")
a("MARKDOWN_CODE_BLOCK", fg, bg="1e2030")
a("MARKDOWN_CODE_FENCE", dark5)
a("MARKDOWN_CODE_SPAN_MARKER", dark5)
a("MARKDOWN_LINK_TEXT", cyan)
a("MARKDOWN_LINK_DESTINATION", blue, effect=blue, effect_type=1)
a("MARKDOWN_LINK_LABEL", blue1)
a("MARKDOWN_AUTO_LINK", cyan, effect=cyan, effect_type=1)
a("MARKDOWN_LIST_ITEM", orange)
a("MARKDOWN_BLOCK_QUOTE", dark5, style=ITALIC)
a("MARKDOWN_BLOCK_QUOTE_MARKER", yellow)
a("MARKDOWN_HRULE", dark3)
a("MARKDOWN_TABLE_SEPARATOR", dark5)

# --- SQL ---
a("SQL_KEYWORD", magenta, style=ITALIC)
a("SQL_TYPE", blue1)
a("SQL_STRING", green)
a("SQL_NUMBER", orange)
a("SQL_COLUMN", green1)
a("SQL_TABLE", blue1)
a("SQL_SCHEMA", blue1, style=ITALIC)
a("SQL_DATABASE_OBJECT", blue1)
a("SQL_PROCEDURE", blue)
a("SQL_LOCAL_ALIAS", yellow)
a("SQL_SYNTHETIC_ENTITY", fg_dark)
a("SQL_PARAMETER", yellow)
a("SQL_LINE_COMMENT", comment, style=ITALIC)
a("SQL_BLOCK_COMMENT", comment, style=ITALIC)

# --- Shell ---
a("BASH.VAR_DEF", fg)
a("BASH.VAR_USE", red)
a("BASH.VAR_USE_BUILTIN", red, style=ITALIC)
a("BASH.EXTERNAL_COMMAND", blue)
a("BASH.INTERNAL_COMMAND", blue1)
a("BASH.FUNCTION_DEF_NAME", blue)
a("BASH.HERE_DOC", green)
a("BASH.HERE_DOC_START", magenta)
a("BASH.HERE_DOC_END", magenta)
a("BASH.SUBSHELL_COMMAND", blue1)
a("BASH.REDIRECTION", blue5)
a("BASH.SHEBANG", comment, style=ITALIC)

# --- Regex ---
a("REGEXP.CHAR_CLASS", blue1)
a("REGEXP.META", magenta)
a("REGEXP.QUANTIFIER", orange)
a("REGEXP.BRACKETS", blue6)
a("REGEXP.ESC_CHARACTER", magenta)

# --- Diff / merge ---
a("DIFF_INSERTED", bg="20303b", error_stripe=git_add)
a("DIFF_MODIFIED", bg="1f2231", error_stripe=git_change)
a("DIFF_DELETED", bg="37222c", error_stripe=git_delete)
a("DIFF_CONFLICT", bg="3d2f20", error_stripe=yellow)
a("DIFF_INSERTED_IGNORED", bg="1e272f")
a("DIFF_MODIFIED_IGNORED", bg="1d1f2c")
a("DIFF_DELETED_IGNORED", bg="2b1e27")
a("DIFF_CONFLICT_IGNORED", bg="2c2620")

# --- Console (ANSI colors match Omarchy's Alacritty Tokyo Night) ---
a("CONSOLE_NORMAL_OUTPUT", fg_dark)
a("CONSOLE_ERROR_OUTPUT", red)
a("CONSOLE_SYSTEM_OUTPUT", dark5)
a("CONSOLE_USER_INPUT", green, style=ITALIC)
a("LOG_ERROR_OUTPUT", red)
a("LOG_WARNING_OUTPUT", yellow)
a("LOG_INFO_OUTPUT", fg_dark)
a("LOG_DEBUG_OUTPUT", dark5)
a("LOG_VERBOSE_OUTPUT", comment)
a("LOG_EXPIRED_ENTRY", comment)
ansi = {
    "BLACK": "15161e", "RED": red, "GREEN": green, "YELLOW": yellow, "BLUE": blue,
    "MAGENTA": magenta, "CYAN": cyan, "WHITE": fg_dark, "GRAY": terminal_black,
    "DARKGRAY": terminal_black,
}
bright = {
    "RED": red, "GREEN": green, "YELLOW": yellow, "BLUE": blue,
    "MAGENTA": magenta, "CYAN": cyan, "WHITE": fg,
}
for k, v in ansi.items():
    a(f"CONSOLE_{k}_OUTPUT", v)
for k, v in bright.items():
    a(f"CONSOLE_{k}_BRIGHT_OUTPUT", v)
a("CONSOLE_GRAY_OUTPUT", terminal_black)
a("CONSOLE_DARKGRAY_OUTPUT", terminal_black)
a("TERMINAL_COMMAND_TO_RUN_USING_IDE", fg=bg, bg=green)

# --- Debugger ---
a("DEBUGGER_INLINED_VALUES", fg=dark5, style=ITALIC)
a("DEBUGGER_INLINED_VALUES_MODIFIED", fg=orange, style=ITALIC)
a("DEBUGGER_INLINED_VALUES_EXECUTION_LINE", fg=blue, style=ITALIC)
a("DEBUGGER_SMART_STEP_INTO_TARGET", bg="2e3c64")
a("DEBUGGER_SMART_STEP_INTO_SELECTION", bg="3d59a1")

# --- Rainbow brackets (built-in) ---
for i, col in enumerate([yellow, magenta, blue, green1, orange], start=1):
    a(f"RAINBOW_COLOR{i}", col)


def render(name="Tokyo Night (Omarchy)"):
    out = [f'<scheme name={quoteattr(name)} version="142" parent_scheme="Darcula">']
    out.append('  <metaInfo>')
    out.append('    <property name="ide">PhpStorm</property>')
    out.append('    <property name="originalScheme">Tokyo Night (Omarchy)</property>')
    out.append('  </metaInfo>')
    out.append('  <option name="FONT_SCALE" value="1.0" />')
    out.append('  <option name="LINE_SPACING" value="1.2" />')
    out.append('  <option name="EDITOR_FONT_SIZE" value="13" />')
    out.append('  <option name="EDITOR_FONT_NAME" value="JetBrains Mono" />')
    out.append('  <option name="EDITOR_LIGATURES" value="true" />')
    out.append('  <colors>')
    for k, v in sorted((k, v) for k, v in colors.items() if v):
        out.append(f'    <option name={quoteattr(k)} value="{v}" />')
    out.append('  </colors>')
    out.append('  <attributes>')
    for k, d in sorted(attrs.items()):
        out.append(f'    <option name={quoteattr(k)}>')
        out.append('      <value>')
        if d["fg"]:
            out.append(f'        <option name="FOREGROUND" value="{d["fg"]}" />')
        if d["bg"]:
            out.append(f'        <option name="BACKGROUND" value="{d["bg"]}" />')
        if d["style"]:
            out.append(f'        <option name="FONT_TYPE" value="{d["style"]}" />')
        if d["stripe"]:
            out.append(f'        <option name="ERROR_STRIPE_COLOR" value="{d["stripe"]}" />')
        if d["effect"]:
            out.append(f'        <option name="EFFECT_COLOR" value="{d["effect"]}" />')
            out.append(f'        <option name="EFFECT_TYPE" value="{d["effect_type"] or 0}" />')
        out.append('      </value>')
        out.append('    </option>')
    out.append('  </attributes>')
    out.append('</scheme>')
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    with open(sys.argv[1], "w") as f:
        f.write(render())
