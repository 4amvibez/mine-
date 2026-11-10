from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.background_color = "#F1E3C2"

INK, ACC, TEAL = "#2B2118", "#D9572B", "#1F6F78"
JP = "IPAGothic"


class HaWa(Scene):
    def construct(self):
        ha = Text("は", font=JP, color=INK, weight=BOLD).scale(5).shift(UP * 3.2)
        self.play(Write(ha), run_time=1.2)

        say = Text('"ha"', font="DejaVu Sans", color=INK, weight=BOLD).scale(1.4).next_to(ha, DOWN, buff=0.6)
        self.play(FadeIn(say, shift=UP * 0.3))
        wa = Text('"wa"?!', font="DejaVu Sans", color=ACC, weight=BOLD).scale(1.4).move_to(say)
        self.play(TransformMatchingShapes(say, wa), ha.animate.set_color(ACC), run_time=0.9)
        self.wait(0.4)

        # timeline of the sound change
        line = NumberLine(x_range=[700, 2000, 100], length=7.6, color=INK, include_ticks=False).shift(DOWN * 2.2)
        self.play(Create(line), run_time=0.8)
        pts = [(700, "pa", INK), (1000, "fa → wa", TEAL), (1946, "rule!", ACC)]
        for year, txt, col in pts:
            d = Dot(line.n2p(year), radius=0.14, color=col)
            y = Text(str(year), font="DejaVu Sans", color=INK).scale(0.45).next_to(d, DOWN, buff=0.25)
            l = Text(txt, font="DejaVu Sans", color=col, weight=BOLD).scale(0.6).next_to(d, UP, buff=0.3)
            self.play(GrowFromCenter(d), FadeIn(y), Write(l), run_time=0.6)
        self.wait(0.5)

        # the three kept particles
        trio = VGroup(*[
            VGroup(Text(k, font=JP, color=ACC, weight=BOLD).scale(1.8),
                   Text(f'= "{r}"', font="DejaVu Sans", color=INK, weight=BOLD).scale(0.8)).arrange(DOWN, buff=0.35)
            for k, r in (("は", "wa"), ("を", "o"), ("へ", "e"))
        ]).arrange(RIGHT, buff=1.1).shift(DOWN * 5.3)
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.4) for g in trio], lag_ratio=0.35), run_time=1.4)
        box = SurroundingRectangle(trio, color=TEAL, buff=0.35, corner_radius=0.2, stroke_width=6)
        self.play(Create(box), run_time=0.7)
        self.wait(1.2)
