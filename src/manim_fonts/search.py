import requests
from .utils import gen_fonts_google_url

def search_font(font_family: str) -> bool:
    # check if https://fonts.google.com/download?family=<name>
    # is returning 200
    font_url = gen_fonts_google_url(font_family)
    c = requests.get(font_url)
    return c.status_code is not 404
