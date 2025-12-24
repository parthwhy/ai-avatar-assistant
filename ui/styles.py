"""
UI Styles and Theme Configuration
Replicating 'Axora' Design: Ultra Dark, Minimalist, Premium.
"""

# Axora Theme Palette
COLOR_BG_MAIN = "#050505"      # Almost black
COLOR_BG_SIDEBAR = "#000000"   # Pure black sidebar
COLOR_BG_CARD = "#141414"      # Dark grey for cards/input
COLOR_BG_CARD_HOVER = "#1f1f1f"
COLOR_ACCENT = "#ffffff"       # White accents
COLOR_TEXT = "#ffffff"
COLOR_TEXT_DIM = "#666666"     # Very dimmed secondary text
COLOR_BORDER = "#222222"       # Subtle borders

# Fonts
FONT_FAMILY = "Segoe UI" 
FONT_LOGO = (FONT_FAMILY, 22, "bold")
FONT_HK = (FONT_FAMILY, 32, "bold") # Hero Header
FONT_SUB = (FONT_FAMILY, 15)
FONT_BODY = (FONT_FAMILY, 13)
FONT_ICON = ("Segoe UI Emoji", 16)

# Dimensions
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
CORNER_RADIUS = 20
SIDEBAR_WIDTH = 260
INPUT_HEIGHT = 100             # Large input box

# Theme config
THEME_JSON = {
    "CTk": {
        "fg_color": COLOR_BG_MAIN
    },
    "CTkFrame": {
        "corner_radius": CORNER_RADIUS,
        "border_width": 0,
        "fg_color": COLOR_BG_CARD,
    },
    "CTkButton": {
        "corner_radius": 10,
        "border_width": 0,
        "fg_color": "transparent",
        "hover_color": COLOR_BG_CARD_HOVER,
        "text_color": COLOR_TEXT_DIM,
        "anchor": "w",
        "font": FONT_BODY
    },
    "CTkLabel": {
        "text_color": COLOR_TEXT,
        "font": FONT_BODY
    },
    "CTkEntry": {
        "corner_radius": 12,
        "border_width": 1,
        "border_color": COLOR_BORDER,
        "fg_color": "#0a0a0a",
        "text_color": COLOR_TEXT,
        "placeholder_text_color": COLOR_TEXT_DIM,
        "font": FONT_BODY
    },
    "CTkTextbox": {
        "corner_radius": CORNER_RADIUS,
        "border_width": 1,
        "border_color": COLOR_BORDER,
        "fg_color": COLOR_BG_CARD,
        "text_color": COLOR_TEXT
    }
}
