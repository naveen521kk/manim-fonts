# Manim Fonts

Get fonts on the fly from the internet which can be used with Manim.

<p align="center">
    <a href="https://pypi.org/project/manim-fonts/"><img src="https://img.shields.io/pypi/v/manim.svg?style=flat&logo=pypi" alt="PyPI Latest Release"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
</p>

## Example

```py
from manim import *
from manim_fonts import *
class Example(Scene):
    def construct(self):
        with RegisterFont("Poppins") as fonts:
            a=Text("Hello World",font=fonts[0])
            self.play(Write(a))
```
You can replace `Poppins` with any font available on Google Fonts for example `RegisterFont("Berkshire Swash")`, and this plugin will download that font and add to search path and returns the font names that can be passed to `Text` to directly to use the fonts.

The fonts downloaded are cached and are reused.

## License

This project is license under [BSD 3-Clause License](https://choosealicense.com/licenses/bsd-3-clause/).