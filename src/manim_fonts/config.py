from pathlib import Path

import platformdirs

APP_NAME = "Manim-Fonts"
APP_AUTHOR = "Naveen M K"

APP_DIRS = platformdirs.user_cache_dir(APP_NAME, APP_AUTHOR)

FONTS_DIR = Path(APP_DIRS, "fonts")
