import appdirs
from pathlib import Path

APP_NAME = "Manim-Fonts"
APP_AUTHOR = "Manim Community"

APPS_DIR = appdirs.user_cache_dir(APP_NAME, APP_AUTHOR)

FONTS_DIR = Path(APPS_DIR, "fonts")
