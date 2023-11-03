from manim import *
import numpy as np
import random as rd
import scipy.optimize


class MonteCarloIntegral(Scene):
    def generate_points(
        self, config={"x_min": -1, "x_max": 1, "y_min": -1, "y_max": 1, "n": 10}
    ):
        x_min = config["x_min"]
        x_max = config["x_max"]
        y_min = config["y_min"]
        y_max = config["y_max"]
        n = config["n"]

        points = []
        for i in range(config["n"]):
            x = rd.uniform(0, 1) * (x_max - x_min) + x_min
            y = rd.uniform(0, 1) * (y_max - y_min) + y_min
            points.append({"x": x, "y": y})
        return points

    def plot_function(self, config={"axis": None, "f": None, "x_min": -2, "x_max": 2}):
        axis = config["axis"]
        f = config["f"]
        x_min = config["x_min"]
        x_max = config["x_max"]

        graph = axis.plot(f, x_range=[x_min, x_max])
        graph.set_stroke(GREEN_C, 3)
        return graph

    def color_points(
        self,
        points,
        f,
        axis,
        config={"color_win": GREEN_C, "color_loss": RED_C, "radius": 0.04},
    ):
        radius = config["radius"] if "radius" in config else 0.04
        points_win = []
        color_win = config["color_win"]
        points_loss = []
        color_loss = config["color_loss"]

        color_points = []
        for point in points:
            x = point["x"]
            y = point["y"]
            if y <= f(x):
                win = Dot(axis.c2p(x, y), color=color_win, radius=radius)
                points_win.append(win)
                color_points.append(win)
            else:
                loss = Dot(axis.c2p(x, y), color=color_loss, radius=radius)
                points_loss.append(loss)
                color_points.append(loss)
        return color_points, points_win, points_loss

    def min_max(self, f, config={"x_start": 0, "x_end": 1}):
        x_start = config["x_start"]
        x_end = config["x_end"]
        y_max = scipy.optimize.minimize_scalar(lambda x: -f(x), bounds=[x_start, x_end])
        y_min = scipy.optimize.minimize_scalar(lambda x: f(x), bounds=[x_start, x_end])

        data = {
            "x_min": y_min["x"],
            "x_max": y_max["x"],
            "y_min": y_min["fun"],
            "y_max": -y_max["fun"],
        }
        return data

    def animate_points(self, points, config={"axis": None}):
        axis = config["axis"]
        radius = config["radius"] if "radius" in config else 0.03
        animations = []
        animated_points = []

        for point in points:
            color = point["color"] if "color" in point else YELLOW_C
            draw_point = Dot(
                axis.c2p(point["x"], point["y"]), color=color, radius=radius
            )
            animated_points.append(draw_point)
            animations.append(Create(animated_points[-1]))

        return animations, animated_points

    def construct(self):
        rd.seed(0)
        x_start = 0
        x_end = 7
        n = 500

        def f(x):
            return np.exp(-(x**2)) + np.sin(x) + x**2 / np.sqrt(1 + x**2)

        data = self.min_max(f, config={"x_start": x_start, "x_end": x_end})
        x_min = data["x_min"]
        x_max = data["x_max"]
        y_min = data["y_min"]
        y_max = data["y_max"]

        if y_min < 0:
            lowerbound = 0
        else:
            lowerbound = y_min

        axes = NumberPlane(
            y_range=(lowerbound, y_max),
            x_range=(x_start, x_end),
            x_length=7,
            y_length=5,
            background_line_style=dict(
                stroke_color=GREY_C,
                stroke_width=2,
                stroke_opacity=0.5,
            ),
        ).center()

        axes.x_axis.add_numbers(font_size=24)
        axes.y_axis.add_numbers(num_decimal_places=1, excluding=[0])
        # axes.to_edge(DOWN)
        graph = axes.plot(f, x_range=[x_start, x_end])
        graph.set_stroke(BLUE, 3)

        t2c = {"x": BLUE}
        graph_label = MathTex(
            "f(x) = e^{-x^2} + sin(x) + \dfrac{x^2}{\sqrt{1+x^2}} ", font_size=40
        )
        graph_label.to_edge(UP).shift(0.2 * UP)
        # graph_label.next_to(
        #     graph.point_from_proportion(0.6), 5 * UP + 2 * LEFT, buff=0.1
        # )

        max_point = Dot(axes.c2p(x_max, y_max), color=RED)
        min_point = Dot(axes.c2p(x_min, y_min), color=RED)

        brace_y = Brace(
            VGroup(Dot(axes.c2p(x_max, y_min)), Dot(axes.c2p(x_max, y_max))),
            direction=RIGHT,
        )
        brace_text_y = brace_y.get_text("Height")
        # .get_text("Height")

        brace_x = Brace(VGroup(axes.get_x_axis()), direction=DOWN)
        brace_text_x = brace_x.get_text("Width")
        # brace_text_x.next_to(axes.get_x_axis(), DOWN)

        self.add(axes)
        self.play(Create(graph))
        self.play(Write(graph_label))
        self.play(Create(max_point), Create(min_point))
        self.play(Create(brace_y), Create(brace_x))
        self.play(Write(brace_text_y), Write(brace_text_x))
        self.wait()

        points = self.generate_points(
            config={
                "x_min": x_start,
                "x_max": x_end,
                "y_min": lowerbound,
                "y_max": y_max,
                "n": n,
            }
        )
        animations, animated_points = self.animate_points(points, config={"axis": axes})

        text_points = (
            MathTex("n_{total} = " + str(len(points)), font_size=30)
        ).to_edge(UP)
        self.play(Transform(graph_label, text_points))
        self.play(
            FadeOut(brace_text_y),
            FadeOut(brace_text_x),
            FadeOut(brace_y),
            FadeOut(brace_x),
        )

        for i in range(0, len(animations)):
            self.play(animations[i], run_time=0.02)
        self.wait()

        color_points, color_win, color_loss = self.color_points(points, f, axes)

        animations = []
        for i in range(0, len(color_points)):
            animations.append(Transform(animated_points[i], color_points[i]))

        self.play(*animations, run_time=1)
        self.wait()

        text = (
            MathTex(
                "\int_{0}^{7}f(x)dx = \lim_{n -> \infty}\dfrac{n_{\t{verde}}}{n_{\t{total}}}*\t{Area}",
                font_size=30,
            )
            .to_edge(UP)
            .shift(0.3 * UP)
        )
        self.play(FadeOut(text_points), FadeOut(graph_label), run_time=0.1)
        self.play(FadeIn(text))
        self.wait(1)

        new_text = (
            MathTex(
                "\\int_{0}^{7}f(x)dx\\, \\approx \\,\\dfrac{"
                + str(len(color_win))
                + "}{"
                + str(len(points))
                + "}"
                + "("
                + str(x_end)
                + "-"
                + str(x_start)
                + ").("
                + str(y_max)
                + "- 0"
                + ")",
                font_size=40,
            )
            .arrange(RIGHT)
            .to_edge(UP)
            .shift(0.3 * UP)
        )
        final_text = (
            MathTex(
                "\\int_{0}^{7}f(x)dx\\, \\approx"
                + str(len(color_win) / len(points) * (x_end - x_start) * (y_max - 0)),
                font_size=40,
            )
            .arrange(RIGHT)
            .to_edge(UP)
            .shift(0.3 * UP)
        )

        self.play(FadeOut(text))
        self.play(FadeIn(new_text), run_time=1)
        self.play(FadeOut(new_text), FadeIn(final_text), runtime=1)
        self.wait()


# class Text(Scene):
#     def construct(self):
#         points = np.arange(0, 30)
#         color_win = np.arange(0, 10)
#         x_end = 7
#         s_tart = 0
#         y_max = 10
#         new_text = (
#             MathTex(
#                 "\\int_{0}^{7}f(x)dx\\, \\approx \\,\\dfrac{"
#                 + str(len(color_win))
#                 + "}{"
#                 + str(len(points))
#                 + "}"
#                 + "("
#                 + str(x_end)
#                 + "-"
#                 + str(x_start)
#                 + ").("
#                 + str(y_max)
#                 + "- 0"
#                 + ")",
#                 font_size=40,
#             )
#             .arrange(RIGHT)
#             .to_edge(UP)
#             .shift(0.3 * UP)
#         )
#         final_text = (
#             MathTex(
#                 "\\int_{0}^{7}f(x)dx\\, \\approx"
#                 + str(len(color_win) / len(points) * (x_end - x_start) * (y_max - 0)),
#                 font_size=40,
#             )
#             .arrange(RIGHT)
#             .to_edge(UP)
#             .shift(0.3 * UP)
#         )

#         self.play(FadeIn(new_text), run_time=1)
#         self.play(FadeOut(new_text), FadeIn(final_text), runtime=1)


MonteCarloIntegral().render()
# Text().rende
