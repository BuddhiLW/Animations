from manim import *
import numpy as np


class Sigmoid_example(Scene):
    def sigmoid(self, z, c=1):
        return 1 / (1 + np.exp(-c * z))

    def gompertz(self, z, a=1, b=-1, c=-2):
        return a * np.exp(-b * np.exp(-c * z))

    def construct(self):
        a = 3
        axis = NumberPlane(
            (-1, 1 * a, 1),
            (0, 1, 0.5),
            # background_line_style={
            # }
            x_length=7,
            y_length=5,
            background_line_style=dict(
                stroke_color=GREY_C,
                stroke_width=2,
                stroke_opacity=0.5,
            ),
        )
        axis.x_axis.add_numbers(font_size=20)
        axis.y_axis.add_numbers(num_decimal_places=1, excluding=[0])
        axis.to_edge(DOWN).shift(0.5 * DOWN)

        b_range, c_range = (
            np.arange(1, 4, 1),
            np.arange(1, 6, 1),
        )

        graphs = VGroup()
        graph_labels = VGroup()
        a = 1
        colors = [random_color() for i in range(len(b_range) * len(c_range))]

        index = 0
        for b, c in [(b, c) for b in b_range for c in c_range]:
            i = index
            graph = axis.plot_parametric_curve(
                lambda t: np.array(
                    [t, self.gompertz(t, a=1, b=b, c=c), 0],
                ),
                t_range=[-1, 3],
            )
            graph.set_stroke(colors[i], 3)
            graphs.add(graph)

            graph_label = MathTex(
                "\t{gompertz}: " + "a=" + str(a) + ", b=" + str(b) + ", c=" + str(c),
                font_size=12,
                color=colors[i],
            )
            graph_labels.add(graph_label)

            index += 1

        graph_labels.arrange(DOWN, buff=SMALL_BUFF).to_edge(UP, buff=SMALL_BUFF).shift(
            0.3 * UP
        )
        # .to_edge(UP).shift(0.2 * UP)

        self.play(Create(axis))
        old = None
        for i in range(len(graphs.submobjects)):
            self.play(Create(graphs.submobjects[i]))
            self.play(Write(graph_labels.submobjects[i]))
            self.wait(1)
        # self.play(Write(graph_label))
        # self.wait(1)
        # self.play(Create(graph), run_time=2)
        self.wait(3)


Sigmoid_example().render()
