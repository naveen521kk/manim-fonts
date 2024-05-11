import hashlib
import json
from pathlib import Path
from typing import Dict

from ._logging import logger
from .config import FONTS_DIR


def str2hash(string: str) -> str:
    hash = hashlib.md5(string.encode())
    return hash.hexdigest()


def gen_download_list_url(font_family: str) -> str:
    return f"https://fonts.google.com/download/list?family={font_family}"


def get_downloaded_fonts() -> Dict[str, str]:
    font_file = FONTS_DIR / "fonts.json"
    if font_file.exists():
        with open(font_file) as f:
            return json.load(f)
    return {}


def update_downloaded_fonts(font_hash, save_path: Path):
    font_file = FONTS_DIR / "fonts.json"
    downloaded = get_downloaded_fonts()
    files = []
    for file in save_path.glob("*.ttf"):
        files.append(str(file))
    downloaded[font_hash] = files
    logger.info("Updating hash")
    with open(font_file, "w") as f:
        json.dump(downloaded, f)
