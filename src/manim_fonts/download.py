import shutil
import tempfile
import time
import zipfile
from pathlib import Path

import requests

from ._logging import logger
from .config import FONTS_DIR
from .utils import (
    gen_fonts_google_url,
    get_downloaded_fonts,
    str2hash,
    update_downloaded_fonts,
)


def download(url: str, local_filename: Path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def download_and_retry(url: str, local_filename: Path):
    logger.info("Downloading %s to %s", url, local_filename)
    for i in range(3):
        logger.info("Try: %s/3", i + 1)
        try:
            download(url, local_filename)
            break
        except (requests.HTTPError, requests.ConnectionError) as e:
            time.sleep(1)
            logger.debug(e)

    else:
        raise requests.HTTPError("%s can't be downloaded" % url)
    return True


def download_fonts(font_family: str) -> Path:
    font_url = gen_fonts_google_url(font_family)
    font_hash = str2hash(font_family)
    font_location = FONTS_DIR / font_hash
    font_location.mkdir(parents=True, exist_ok=True)
    if font_hash not in get_downloaded_fonts():
        logger.info("Downloading %s from %s", font_family, font_url)
        with tempfile.TemporaryDirectory(prefix="manim-fonts") as tmpdir:
            tfile = Path(tmpdir) / "temp.zip"
            download_and_retry(font_url, tfile)
            with zipfile.ZipFile(tfile, "r") as zip:
                zip.extractall(tmpdir)
            for file in Path(tmpdir).glob("*.ttf"):
                logger.info("Moving %s to %s", file, font_location)
                shutil.copy(file, font_location)
        update_downloaded_fonts(font_hash, font_location)
    return font_location
