from manim import *

from manim_fonts import *


class TestFonts(Scene):
    def construct(self):
        with RegisterFont("Caveat") as things:
            a = Text("Hello World", font=things[0])
            self.play(Write(a))
