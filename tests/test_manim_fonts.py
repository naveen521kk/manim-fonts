import json
from pathlib import Path

import appdirs
import pytest


@pytest.fixture
def new_fonts_dir(tmpdir, monkeypatch):
    tmpdir = Path(tmpdir)

    def tmp(*args):
        return tmpdir

    monkeypatch.setattr(appdirs, "user_cache_dir", tmp)
    yield tmpdir


def test_download(new_fonts_dir):
    from manim_fonts import RegisterFont
    from manim_fonts.config import FONTS_DIR

    assert FONTS_DIR == new_fonts_dir / "fonts"
    with RegisterFont("Odibee Sans") as f:
        assert f
        assert Path(FONTS_DIR).exists()
        assert list(Path(FONTS_DIR).glob("*"))
        assert Path(FONTS_DIR) / "fonts.json"
        assert json.load((Path(FONTS_DIR) / "fonts.json").open())
