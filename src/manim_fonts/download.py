import json
import shutil
import tempfile
import time
from pathlib import Path

import requests

from ._logging import logger
from .config import FONTS_DIR
from .utils import (
    gen_download_list_url,
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


def download_font_files(font_family: str, tmpdir: Path) -> None:
    font_url = gen_download_list_url(font_family)
    res = requests.get(font_url)
    res.raise_for_status()

    # find first { and string contents before it
    contents = res.text
    start = contents.find("{")
    contents = contents[start:]

    fonts = json.loads(contents)
    file_refs = fonts.get("manifest", {}).get("fileRefs", None)

    if not file_refs:
        raise ValueError("No valid font files fount for font family %s" % font_family)

    logger.info(
        "Downloading font files for %s (number of font_file=%d)",
        font_family,
        len(file_refs),
    )
    for file in file_refs:
        url = file.get("url")
        filename = file.get("filename")
        download_dest = tmpdir / filename

        # if folder is not created, create it
        download_dest.parent.mkdir(parents=True, exist_ok=True)
        download_and_retry(url, tmpdir / filename)


def download_fonts(font_family: str) -> Path:
    font_hash = str2hash(font_family)
    font_location = FONTS_DIR / font_hash
    font_location.mkdir(parents=True, exist_ok=True)
    if font_hash not in get_downloaded_fonts():
        logger.info(
            "Downloading %s font from google fonts to %s", font_family, font_location
        )
        with tempfile.TemporaryDirectory(prefix="manim-fonts") as tmpdir:
            try:
                download_font_files(font_family, Path(tmpdir))
            except requests.HTTPError as e:
                error_message = (
                    "Error while downloading font files for font family %s"
                    % font_family
                )
                error_message += "\n" + repr(e)
                error_message += (
                    "\n" + "Please check if the font family is correct and try again."
                )
                error_message += (
                    "\n" + "If the issue persists, please report it at"
                    " https://github.com/naveen521kk/manim-fonts/issues"
                )
                logger.error(error_message)
                raise Exception(error_message)
            for file in Path(tmpdir).glob("*.ttf"):
                logger.info("Moving %s to %s", file, font_location)
                shutil.copy(file, font_location)
        update_downloaded_fonts(font_hash, font_location)
    return font_location
