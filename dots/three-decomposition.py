from manim import *
import math


def create_dots(n, m, *args, color=BLUE, rounding_box=False):
    all_dots = VGroup()

    if args:
        print(args)
        print(args[0])
        x_plus = args[0]
        j = math.floor(x_plus / n)
        remainder = x_plus % n
        all_dots = (
            create_dots(n, m, color=color)
            .add(create_dots(n, j, color=GREEN).shift([n + 1, 0, 0]))
            .add(create_dots(1, remainder, color=YELLOW_A).shift([m + j, 0, 0]))
            .shift([-(m + m / j), 0, 0])
        )

        return all_dots

    else:
        for i in range(n):
            dots = VGroup()
            for j in range(m):
                dots.add(Dot([j, i, 0], color=color))
                all_dots.add(dots)

        return all_dots


def create_rouding_boxes(vgroups, *args, color=YELLOW):
    boxes = VGroup()
    if args:
        n = len(list(vgroups))
        m = len(list(vgroups[0]))
        for j in range(m):
            box = VGroup()
            for i in range(n):
                box.add(vgroups[i][j])
            boxes.add(SurroundingRectangle(box, buff=0.1, color=color))
        return boxes

    else:
        for vgroup in vgroups:
            boxes.add(SurroundingRectangle(vgroup, buff=0.1, color=color))
        return boxes

    # boxes = VGroup()
    # for vgroup in vgroups:
    #     boxes.add(SurroundingRectangle(vgroup, buff=0.1))
    # return boxes
    #


def create_3d_dots(n, m, l, *args, color=BLUE, rounding_box=False):
    all_dots = VGroup()

    if args:
        print(args)
        print(args[0])
        x_plus = args[0]
        j = math.floor(x_plus / n)
        remainder = x_plus % n
        all_dots = (
            create_dots(n, m, color=color)
            .add(create_dots(n, j, color=GREEN).shift([n + 1, 0, 0]))
            .add(create_dots(1, remainder, color=YELLOW_A).shift([m + j, 0, 0]))
            .shift([-(m + m / j), 0, 0])
        )

        return all_dots

    else:
        for i in range(n):
            dots = VGroup()
            for j in range(m):
                dots_2d = VGroup()
                for k in range(l):
                    dots_2d.add(Dot3D(point=[j, i, k], radius=0.12, color=color))
                dots.add(dots_2d)
            all_dots.add(dots)

        return all_dots


class ThreeDDots(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()

        all_dots = create_dots(3, 4, color=BLUE)
        framebox0 = SurroundingRectangle(all_dots, buff=0.1)
        framebox1 = create_rouding_boxes(all_dots, "down", color=GREEN)
        framebox2 = create_rouding_boxes(all_dots, color=RED)
        # framebox3 = create_rouding_boxes(all_dots[0:1], "down", color=GREEN)
        # framebox4 = create_rouding_boxes(all_dots[1:2], "down", color=GREEN)
        # self.add(group, dest)
        self.add(all_dots)
        self.play(Create(framebox0))
        self.play(Transform(framebox0, framebox1))
        self.play(FadeOut(framebox0))
        self.play(Create(framebox2))
        self.play(FadeOut(framebox2))
        # self.play(Create(framebox3))
        # self.play(Create(framebox4))
        self.play(FadeOut(all_dots))

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        all_dots = create_3d_dots(3, 2, 2, color=BLUE)
        self.play(Create(all_dots))
        self.wait(4)


ThreeDDots().render()
