import requests
from pathlib import Path
import zipfile
from .config import FONTS_DIR
from .utils import gen_fonts_google_url,str2hash,get_downloaded_fonts,update_downloaded_fonts
import tempfile
import shutil
from ._logging import logger


def download_fonts(font_family: str) -> Path:
    font_url = gen_fonts_google_url(font_family)
    font_hash = str2hash(font_family)
    font_location = FONTS_DIR / font_hash
    font_location.mkdir(parents=True, exist_ok=True)
    if font_hash not in get_downloaded_fonts():
        logger.info("Downloading %s from %s", font_family, font_url)
        con = requests.get(font_url)
        con.raise_for_status()
        with tempfile.TemporaryDirectory(prefix="manim-fonts") as tmpdir:
            tfile = Path(tmpdir) / "temp.zip"
            with open(tfile, "wb") as f:
                f.write(con.content)
            with zipfile.ZipFile(tfile, "r") as zip:
                zip.extractall(tmpdir)
            for file in Path(tmpdir).glob("*.ttf"):
                logger.info("Moving %s to %s", file, font_location)
                shutil.copy(file, font_location)
        update_downloaded_fonts(font_hash,font_location)
    return font_location
