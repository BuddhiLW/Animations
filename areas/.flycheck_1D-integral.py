from manim import *
import numpy as np


class Integral1D(Scene):
    def animate_list(self, animations, **kwargs):
        time_anim = kwargs["time_anim"] if "time_anim" in kwargs else 1
        time_subanim = kwargs["time_subanim"] if "time_subanim" in kwargs else 0.5
        time_subsubanim = (
            kwargs["time_subsubanim"] if "time_subsubanim" in kwargs else 0.25
        )
        depth = kwargs["depth"] if "depth" in kwargs else 1

        for anim in animations:
            if isinstance(anim, list):
                self.animate_list(
                    anim,
                    depth=depth + 1,
                    time_anim=time_anim,
                    time_subanim=time_subanim,
                    time_subsubanim=time_subsubanim,
                )
            else:
                if depth == 1:
                    self.play(anim)
                elif depth == 2:
                    self.play(anim, run_time=time_subanim)
                elif depth == 3:
                    self.play(anim, run_time=time_subsubanim)
                else:
                    self.play(anim, run_time=time_subsubanim)

    def construct(self):
        a = 1
        axis = NumberPlane(
            (-1.5 * a, 1.5 * a, 0.5),
            (-1.5 * a, 1.5 * a, 0.5),
            # background_line_style={
            # }
            x_length=4,
            y_length=4,
            background_line_style=dict(
                stroke_color=GREY_C,
                stroke_width=2,
                stroke_opacity=0.5,
            ),
        )
        axis.x_axis.add_numbers(font_size=20)
        axis.y_axis.add_numbers(num_decimal_places=1, excluding=[0])
        axis.to_edge(DOWN).shift(0.5 * DOWN)
        graph = axis.plot_parametric_curve(
            lambda t: np.array(
                [a * (np.cos(t) ** 3), a * (np.sin(t) ** 3), 0],
            ),
            t_range=[0, 2 * PI],
        )
        graph.set_stroke(BLUE, 3)

        t2c = {"x": BLUE}
        graph_label = MathTex(
            "\t{Astroid}: x^{\\frac{2}{3}} + y^{\\frac{2}{3}} = a^{\\frac{2}{3}}",
            font_size=32,
        )
        graph_label.to_edge(UP).shift(0.2 * UP)

        self.play(Create(axis))
        self.play(Write(graph_label))
        self.wait(1)
        self.play(Create(graph), run_time=2)
        self.wait(1)

        integral_text = MathTex(
            "S=\\int_{a}^{b}\\sqrt{1 + \\left(\\frac{dy}{dx}\\right)^2}dx",
            font_size=32,
        )
        implication = MathTex(
            "\\land \\quad \\dfrac{dy}{dx} = - \\dfrac{y^{\\frac{1}{3}}}{x^{\\frac{1}{3}}}",
            font_size=32,
        )
        texts = VGroup(graph_label, integral_text, implication)
        texts.arrange(DOWN).to_edge(UP, buff=MED_SMALL_BUFF)
        # self.play(FadeOut(graph_label))
        for word in texts.submobjects:
            self.play(Write(word))
            self.wait(0.2)
        self.wait(1)

        implication_new = MathTex(
            "\\implies S=\\int_{a}^{b}\\sqrt{1 + \\left(\\frac{y^{\\frac{2}{3}}}{x^{\\frac{2}{3}}}\\right)}dx",
            font_size=32,
        )
        texts_new = VGroup(texts.submobjects[1], texts.submobjects[2], implication_new)
        texts_new.arrange(DOWN).to_edge(UP, buff=MED_SMALL_BUFF)
        self.play(TransformMatchingTex(texts, texts_new))
        self.wait(1)
        graph_label_new = MathTex(
            "x^{\\frac{2}{3}} + y^{\\frac{2}{3}} = a^{\\frac{2}{3}} \\implies y^{\\frac{2}{3}} = a^{\\frac{2}{3}} - x^{\\frac{2}{3}}",
            font_size=32,
        )
        implication = MathTex(
            "\\implies 4\\left(\\int_{0}^{a}{\\dfrac{a^{\\frac{1}{3}}}{x^\\frac{1}{3}}}dx\\right)=4*(\\frac{3}{2}.a)",
            font_size=32,
        )
        texts = VGroup(texts_new.submobjects[2], graph_label_new, implication)
        texts.arrange(DOWN).to_edge(UP, buff=MED_SMALL_BUFF)
        self.play(TransformMatchingTex(texts_new, texts))
        self.wait(1)

        final_implication = MathTex("S=6.a", font_size=35).to_edge(
            UP, buff=MED_SMALL_BUFF
        )
        self.play(Transform(texts, final_implication))
        self.wait(1)



        a = 1
        axis_new = NumberPlane(
            (-1.5 * a, 1.5 * a, 0.5),
            (-1.5 * a, 1.5 * a, 0.5),
            # background_line_style={
            # }
            x_length=4,
            y_length=4,
            background_line_style=dict(
                stroke_color=GREY_C,
                stroke_width=2,
                stroke_opacity=0.5,
            ),
        )
        axis_new.x_axis.add_numbers(font_size=20)
        axis_new.y_axis.add_numbers(num_decimal_places=1, excluding=[0])
        axis_new.to_edge(DOWN).shift(0.5 * DOWN)
        graph_new = axis_new.plot_parametric_curve(
            lambda t: np.array(
                [a * (np.cos(t) ** 3), a * (np.sin(t) ** 3), 0],
            ),
            t_range=[0, 2 * PI],
        )
        graph.set_stroke(BLUE, 3)

        t2c = {"x": BLUE}
        graph_label = MathTex(
            "\t{Astroid}: x^{\\frac{2}{3}} + y^{\\frac{2}{3}} = a^{\\frac{2}{3}}",
            font_size=32,
        )
        graph_label.to_edge(UP).shift(0.2 * UP)

        self.play(Create(axis))
        self.play(Write(graph_label))
        self.wait(1)
        self.play(Create(graph), run_time=2)
        self.wait(1)


Integral1D().render()
