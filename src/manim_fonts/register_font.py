from contextlib import contextmanager

import manimpango

from ._logging import logger
from .download import download_fonts


@contextmanager
def RegisterFont(font_family):
    pth = download_fonts(font_family)
    orig_font = manimpango.list_fonts()
    for file in pth.glob("*.ttf"):
        if not manimpango.register_font(str(file.absolute())):
            logger.warning("Error registering %s", file)
    new_font = manimpango.list_fonts()
    fonts_names = list(set(new_font) - set(orig_font))
    logger.info("Found fonts %s", fonts_names)
    if fonts_names == []:
        logger.warning("No fonts registered")
    try:
        yield fonts_names
    finally:
        for file in pth.glob("*.ttf"):
            manimpango.unregister_font(str(file))
