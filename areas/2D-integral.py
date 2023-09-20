from manim import *
import numpy as np


class Integral(Scene):
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
        axes = NumberPlane(
            (-4, 4),
            (0, 1.5, 0.5),
            # background_line_style={
            # }
            x_length=14,
            y_length=5,
            background_line_style=dict(
                stroke_color=GREY_C,
                stroke_width=2,
                stroke_opacity=0.5,
            ),
        )
        axes.x_axis.add_numbers(font_size=24)
        axes.y_axis.add_numbers(num_decimal_places=1, excluding=[0])
        axes.to_edge(DOWN)
        graph = axes.plot(lambda x: np.exp(-(x**2)))
        graph.set_stroke(BLUE, 3)

        t2c = {"x": BLUE}
        graph_label = MathTex("e^{-x^2}", font_size=50)
        graph_label.next_to(graph.point_from_proportion(0.6), 3 * UR)

        self.add(axes)
        self.play(Create(graph))
        self.play(Write(graph_label))
        self.wait()

        # # Show integral
        integral = MathTex(R"\int_{-\infty}^\infty e^{-x^2} dx")
        integral.to_edge(UP)

        self.play(graph.animate.set_fill(BLUE, 0.5))
        self.wait()
        self.play(
            Write(integral),
            # FadeTransform(graph_label.copy(), integral["e^{-x^2}"]),
        )
        # self.play(TransformFromCopy(integral["x"][0], integral["dx"]))
        self.wait()

        # # Show rectangles
        colors = (BLUE_E, BLUE_D, TEAL_D, TEAL_E)
        rects = axes.get_riemann_rectangles(graph, dx=0.2, color=colors)
        rects.set_stroke(WHITE, 1)
        rects.set_fill(opacity=0.75)
        rect = rects[len(rects) // 2 - 2].copy()
        rect.set_opacity(1)
        # graph_label.set_backstroke(width=5)

        brace = Brace(rect, UP, SMALL_BUFF)
        # brace.set_backstroke(width=3)
        dx_label = brace.get_tex("dx", buff=SMALL_BUFF)
        dx_label.set_color_by_tex("x", BLUE)

        axes.generate_target()
        axes.target.y_axis.numbers.set_opacity(0)

        self.play(
            FadeIn(rects, lag_ratio=0.1, run_time=3),
            Transform(graph.copy(), graph.set_fill(opacity=0)),
            Transform(graph_label.copy(), graph_label.shift(SMALL_BUFF * UR)),
            Create(graph_label),
            Create(brace),
        )
        # self.wait()

        animations = []
        # Thinner rectangles
        self.play(Create(dx_label))
        for dx in [0.1, 0.075, 0.05, 0.03, 0.02, 0.01, 0.005]:
            new_rects = axes.get_riemann_rectangles(graph, dx=dx, color=colors)
            new_rect = new_rects[len(new_rects) // 2 - 2].copy()
            new_rects.set_stroke(WHITE, 1)
            new_rects.set_fill(opacity=0.7)
            width = dx * axes.x_axis.unit_size
            new_brace = Brace(new_rect, UP, SMALL_BUFF)

            # brace = Brace(rect, UP, SMALL_BUFF)
            # brace.set_backstroke(width=3)
            new_dx_label = new_brace.get_tex("dx", buff=SMALL_BUFF)
            new_dx_label.set_color_by_tex("x", BLUE)

            subanimations = []
            subanimations.append(Transform(rects, new_rects))
            subsubanimations = []
            subsubanimations.append(
                Transform(
                    brace,
                    new_brace,
                )
            )
            subsubanimations.append(Transform(dx_label, new_dx_label))
            subanimations.append(subsubanimations)
            subanimations.append(FadeOut(brace))
            subanimations.append(FadeOut(dx_label))
            animations.append(subanimations)
            brace = new_brace
            dx_label = new_dx_label

        self.animate_list(animations)
        # for anim in animations:
        #     self.play(anim)
        self.add(graph)
        self.play(
            FadeOut(brace),
            FadeOut(new_brace),
            FadeOut(dx_label),
            Create(graph),
        )


Integral().render()
