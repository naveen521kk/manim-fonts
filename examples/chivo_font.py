from manim import *

from manim_fonts import *


class TestFonts(Scene):
    def construct(self):
        with RegisterFont("Chivo") as things:
            a = Text(str(things), font=things[0], weight=HEAVY).scale(0.5)
            self.play(Write(a))
            self.wait(0.6)
