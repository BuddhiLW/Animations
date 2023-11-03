from manim import *
import math
from sympy.ntheory import factorint
from itertools import chain
import numpy as np
from functools import cmp_to_key


def create_random_dots(n, *args, **kwargs):
    np.random.seed(0)  ## Cache
    color = kwargs["config"]["color"]
    all_dots = VGroup()
    rand_positions_x = np.random.normal(0.5, 4, (n, 1))
    rand_positions_y = np.random.normal(0, 2, (n, 1))
    for i in range(n):
        position = np.concatenate([rand_positions_x[i], rand_positions_y[i], [0]])
        dot = Dot(position, color=color)
        all_dots.add(dot)

    return all_dots


def slope(p1, p2):
    if p1[0] == p2[0]:
        return float("inf")
    else:
        return 1.0 * (p1[1] - p2[1]) / (p1[0] - p2[0])


def cross_product(p1, p2, p3):
    return ((p2[0] - p1[0]) * (p3[1] - p1[1])) - ((p2[1] - p1[1]) * (p3[0] - p1[0]))


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def orientation(p, q, r):
    val = cross_product(p, q, r)
    if val == 0:
        return 0  # collinear
    elif val > 0:
        return 1  # clock wise
    else:
        return 2  # counterclock wise


# # A function used by cmp_to_key function to sort an array of
# points with respect to the first point
def compare(p1, p2, **kwargs):
    p0 = kwargs["p0"]
    # Find orientation
    o = orientation(p0.get_center(), p1.get_center(), p2.get_center())
    if o == 0:
        if distance(p0.get_center(), p2.get_center()) >= distance(
            p0.get_center(), p1.get_center()
        ):
            return -1
        else:
            return 1
    else:
        if o == 2:
            return -1
        else:
            return 1


def graham_scan(vgroup):
    # =vgroup=: a VGroup of Dot objects
    animation_sequence = []
    points = vgroup.submobjects

    ## find the lowest point
    points.sort(key=lambda x: [x.get_center()[0], x.get_center()[1]])
    p0 = points[0]

    ### add the lowest point turning RED, to the animation sequence
    animation_sequence.append(Transform(p0, p0.copy().set_color(RED)))

    ## sort the points by polar angle, in relation to the lowest point
    compare0 = lambda p1, p2: compare(p1, p2, p0=p0)
    points = sorted(points, key=cmp_to_key(compare0))
    # points.sort(
    #     key=lambda p: (
    #         slope(p.get_center(), p0.get_center()),
    #         p.get_center()[2],
    #         p.get_center()[1],
    #     ),
    # )

    ### add the sorted points turning GREEN, to the animation sequence
    animation_sequence.append(
        Transform(VGroup(*points), VGroup(*points).set_color(GREEN))
    )

    ## initialize the hull
    hull = [p0, points[1], points[2]]
    animation_sequence.append(Transform(VGroup(*hull), VGroup(*hull).set_color(RED)))

    for i in range(3, len(points)):
        animation_package = []
        while (len(hull) > 1) and (
            orientation(
                hull[-2].get_center(), hull[-1].get_center(), points[i].get_center()
            )
            != 2
        ):
            ### add animation of the triangle formed by the last three points
            triangle = Polygon(
                hull[-2].get_center(),
                hull[-1].get_center(),
                points[i].get_center(),
                color=BLUE_A,
                fill_opacity=0.5,
                fill_color=PURPLE_A,
            )
            animation_package.append(Create(triangle))
            # animation_sequence.append(
            popped = hull.pop()
            ### add the points that are not part of the hull, turning BLUE, to the animation sequence
            animation_package.append(FadeOut(triangle))
            animation_package.append(Transform(popped, popped.copy().set_color(BLUE)))
            animation_sequence.append(animation_package)

        hull.append(points[i])
        ### add the points that are part of the hull, turning RED_A, to the animation sequence
        ### add animation of the triangle formed by the last three points
        triangle = Polygon(
            hull[-2].get_center(),
            hull[-1].get_center(),
            points[i].get_center(),
            color=BLUE_A,
            fill_opacity=0.5,
            fill_color=MAROON_A,
        )
        animation_package.append(Create(triangle))
        animation_package.append(Transform(points[i], points[i].copy().set_color(RED)))
        animation_package.append(FadeOut(triangle))
        animation_sequence.append(animation_package)

    return hull, animation_sequence
    # while len(hull) > 2 and get_cross_product(hull[-3], hull[-2], hull[-1]) < 0:
    #     hull.pop(-2)


def create_polygon(hull):
    points = [p.get_center() for p in hull]
    polygon = Polygon(*points, color=WHITE)
    return polygon


def rotatingCaliper(convex_hull_points):
    # Takes O(n)
    # convex_hull_points = convexHull(points)
    n = len(convex_hull_points)
    print("convex_hull_points: ", convex_hull_points)
    print("n: ", n)
    animation_sequence = []

    # Convex hull point in counter-clockwise order
    hull = convex_hull_points
    # for i in range(n):
    #     hull.append(convex_hull_points[i])

    # Base Cases
    if n == 1:
        return 0
    if n == 2:
        return distance(hull[0].get_center(), hull[1].get_center())
    k = 1

    # Find the farthest vertex
    # from hull[0] and hull[n-1]
    text = Text(f"Achar pontas mais longinquas", font_size=24).to_edge(UP)
    animation_sequence.append(Create(text))
    while abs(
        cross_product(
            hull[n - 1].get_center(),
            hull[0].get_center(),
            hull[(k + 1) % n].get_center(),
        )
    ) > abs(
        cross_product(
            hull[n - 1].get_center(), hull[0].get_center(), hull[k].get_center()
        )
    ):
        area1 = Polygon(
            hull[n - 1].get_center(),
            hull[0].get_center(),
            hull[(k + 1) % n].get_center(),
            color=YELLOW_C,
            fill_opacity=0.5,
            fill_color=YELLOW_C,
        )
        area2 = Polygon(
            hull[n - 1].get_center(),
            hull[0].get_center(),
            hull[k].get_center(),
            color=YELLOW,
            fill_opacity=0.5,
            fill_color=YELLOW,
        )
        animation_sequence.append(Create(area1))
        animation_sequence.append(Create(area2))
        animation_sequence.append(FadeOut(area1))
        animation_sequence.append(FadeOut(area2))
        k += 1

    res = 0
    extreme_points = []

    text2 = Text(f"Achar maior distância, das pontas", font_size=24).to_edge(UP)
    animation_sequence.append(Transform(text, text2))
    # Check points from 0 to k
    max_line = Line(*[hull[0].get_center(), hull[k].get_center()])
    animation_sequence.append(Create(max_line))
    for i in range(k + 1):
        j = (i + 1) % n
        while abs(
            cross_product(
                hull[i].get_center(),
                hull[(i + 1) % n].get_center(),
                hull[(j + 1) % n].get_center(),
            )
        ) > abs(
            cross_product(
                hull[i].get_center(),
                hull[(i + 1) % n].get_center(),
                hull[j].get_center(),
            )
        ):
            area1 = Polygon(
                hull[i].get_center(),
                hull[(i + 1) % n].get_center(),
                hull[(j + 1) % n].get_center(),
                color=YELLOW_C,
                fill_opacity=0.5,
                fill_color=YELLOW_C,
            )
            area2 = Polygon(
                hull[i].get_center(),
                hull[(i + 1) % n].get_center(),
                hull[j].get_center(),
                color=YELLOW,
                fill_opacity=0.5,
                fill_color=YELLOW,
            )
            animation_sequence.append(Create(area1))
            animation_sequence.append(Create(area2))
            animation_sequence.append(FadeOut(area1))
            animation_sequence.append(FadeOut(area2))
            # Update res
            if res < distance(hull[i].get_center(), hull[(j + 1) % n].get_center()):
                res = distance(hull[i].get_center(), hull[(j + 1) % n].get_center())
                extreme_points = [hull[i], hull[(j + 1) % n]]

                ## Update max_line (animation only)
                new_max_line = Line(
                    hull[i].get_center(), hull[(j + 1) % n].get_center()
                )
                animation_sequence.append(FadeOut(max_line))
                animation_sequence.append(FadeIn(new_max_line))
                max_line = new_max_line

                j = (j + 1) % n
            else:
                j = (j + 1) % n

            # res = max(
            #     res, distance(hull[i].get_center(), hull[(j + 1) % n].get_center())
            # )
            # Update extreme points
            # extreme_points = [hull[i], hull[(j + 1) % n]]

    # Return the result distance
    animation_sequence.append(FadeOut(text))
    animation_sequence.append(FadeOut(text2))
    animation_sequence.append(FadeOut(max_line))
    return res, extreme_points, animation_sequence


class Distances_2D(Scene):
    def construct(self):
        n = 50
        mean_x, std_x = 0.5, 4
        mean_y, std_y = 0, 2
        text = MathTex(
            "N_{points} = ",
            n,
            ", \quad Distribuicoes: Normal_{x}(",
            mean_x,
            ", ",
            std_x,
            "), \, Normal_{y}(",
            mean_y,
            ", ",
            std_y,
            ")",
            font_size=24,
        ).to_edge(UP)
        all_dots = (
            create_random_dots(n, config={"color": BLUE})
            .scale(0.5)
            .center()
            .shift(DOWN)
        )
        self.play(Write(text))
        self.play(Create(all_dots))
        self.wait(2)

        distances_brute_force = VGroup()
        hull, animations = graham_scan(all_dots)
        # self.play(*animations)

        for animation in animations:
            if isinstance(animation, list):
                for subanimation in animation:
                    self.play(subanimation, run_time=0.05)
            else:
                self.play(animation, run_time=0.5)

        polygon = create_polygon(hull)
        self.play(FadeIn(polygon))
        self.wait(2)

        self.play(FadeOut(text))
        max_distance, extreme_points, animations = rotatingCaliper(hull)

        for animation in animations:
            if isinstance(animation, list):
                for subanimation in animation:
                    self.play(subanimation, run_time=0.05)
            else:
                self.play(animation, run_time=0.05)

        text = Text(f"Distancia maxima: {max_distance}", font_size=24).to_edge(UP)
        self.play(Create(text))
        self.play(
            FadeIn(Line(*[p.get_center() for p in extreme_points], color=PURPLE)),
            FadeOut(polygon),
        )

        self.wait(2)


Distances_2D().render()
# Decompose_2D().render()
# Decompose_1D().render()
# Decompose().render()
# TwoDDots().render()


# for i in range(0, len(hull)):
#     if i == 0:
#         self.play(
#             Create(
#                 Line(hull[-1].get_center(), hull[i].get_center(), color=RED),
#                 run_time=0.5,
#                 stroke_width=1,
#             )
#         )
#     else:
#         self.play(
#             Create(
#                 Line(
#                     hull[i - 1].get_center(),
#                     hull[i].get_center(),
#                     color=RED,
#                     stroke_width=1,
#                 )
#             ),
#             run_time=0.5,
#         )
