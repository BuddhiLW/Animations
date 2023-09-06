from manim import *
import math
from sympy.ntheory import factorint

# from manim_voiceover import VoiceoverScene

# from manim_voiceover.services.gtts import GTTSService
# from manim_voiceover.services.coqui import CoquiService


def create_dots(n, m, *args, **kwargs):
    color = kwargs["color"]
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


def create_rouding_boxes(vgroups, *args, **kwargs):
    """VGroups"""
    print(kwargs)
    color = kwargs["config"]["color"]
    text = kwargs["config"]["text"]

    if kwargs["config"].keys().__contains__("buff"):
        buff = kwargs["config"]["buff"]
    else:
        buff = 0.1

    print(kwargs["config"].keys())
    print(kwargs["config"].keys().__contains__("buff"))
    print("buff size: ", buff)

    if kwargs["config"].keys().__contains__("scale"):
        scale = kwargs["config"]["scale"]
    else:
        scale = 1

    boxes = VGroup()
    if args:
        n = len(list(vgroups))
        m = len(list(vgroups[0]))
        new_text = Text(f"N = {n}*{m}", font_size=24).to_edge(UP).set_color(YELLOW)
        for j in range(m):
            box = VGroup()
            for i in range(n):
                box.add(vgroups[i][j])
                boxes.add(SurroundingRectangle(box, buff=buff, color=color))
        return boxes, new_text

    else:
        n = len(list(vgroups))
        m = len(list(vgroups[0]))
        new_text = Text(f"N = {m}*{n}", font_size=24).to_edge(UP).set_color(YELLOW)
        for vgroup in vgroups:
            boxes.add(SurroundingRectangle(vgroup, buff=buff, color=color))
        return boxes, new_text


def create_rouding_boxes_decomposition(vgroups, *args, **kwargs):
    color = kwargs["config"]["color"]
    text = kwargs["config"]["text"]
    boxes = VGroup()
    n = len(list(vgroups))
    m = len(list(vgroups[0]))

    factorsm = factorint(m)
    factor1 = list(factorsm.keys())[0]
    p = int(m / factor1)

    new_text = (
        Text(f"N = ({factor1}*{p})*{n}", font_size=24).to_edge(UP).set_color(YELLOW)
    )

    for i in range(n):
        box = VGroup()
        for j in range(m):
            if (j + 1) % p == 0:
                box.add(vgroups[i][j])
                boxes.add(SurroundingRectangle(box, buff=0.1, color=color))
                box = VGroup()
            else:
                box.add(vgroups[i][j])
    return boxes, new_text


def create_n_dots(n, **kwargs):
    print(kwargs)
    factors_map = factorint(n)
    factors = list(factors_map.keys())
    factors_values = [factor ** factors_map[factor] for factor in factors]
    if len(factors) >= 2:
        max_factor_value = int(max(factors_values))
        rest_factors = int(n / max_factor_value)
    else:
        if list(factors_map.values())[0] % 2 == 0:
            max_factor_value = int(factors[0] ** (factors_map[factors[0]] / 2))
            rest_factors = int(n / max_factor_value)
        else:
            max_factor_value = int(factors[0] ** math.ceil(factors_map[factors[0]] / 2))
            rest_factors = int(n / max_factor_value)

    return create_dots(max_factor_value, rest_factors, **kwargs)


class TwoDDots(Scene):
    def construct(self):
        n = 5 * 6
        all_dots = create_dots(5, 6, color=BLUE).center()
        text = Text(f"N = {n}", font_size=24).to_edge(UP).set_color(YELLOW)

        framebox0 = SurroundingRectangle(all_dots, buff=0.1)

        factors = factorint(n)
        gratest_factor = max(factors.keys())
        rest_factors = n / gratest_factor

        text1 = (
            Text(f"N = {gratest_factor}*{rest_factors}", font_size=24)
            .to_edge(UP)
            .set_color(YELLOW)
        )
        framebox1, text1 = create_rouding_boxes(
            all_dots, "down", config={"color": GREEN, "text": text}
        )
        framebox2, text2 = create_rouding_boxes(
            all_dots, config={"color": RED, "text": text1, "buff": 0.22}
        )
        framebox3, text3 = create_rouding_boxes_decomposition(
            all_dots, config={"color": PURPLE, "text": text2}
        )
        # self.add(group, dest)
        # self.set_speech_service(
        #     CoquiService()
        # GTTSService(lang="en", tld="com")
        # )  # self.set_speech_service(GTTSService(lang="pt", tld="com.br"))
        # Let's consider 30 dots, and how to group them. The first grouping we may consider is by boxing the 30
        # with self.voiceover(
        #     text="Let's consider 30 dots, and how to group them. We may consider boxing the 30 dots in one group."
        # ) as tracker:
        self.play(
            Create(all_dots),
            Create(framebox0),
            Create(text),
            run_time=tracker.duration,
        )

        # with self.voiceover(
        #     text="Or, we could group them in fives. Given a total of 6 groups."
        # ) as tracker:
        self.play(
            Transform(text, text1),
            Transform(framebox0, framebox1),
            run_time=tracker.duration,
        )

        self.wait(1)
        self.play(FadeOut(text1))
        self.play(FadeOut(framebox0))
        self.play(FadeOut(text))

        # with self.voiceover(
        #     text="In turn, we could group them in sixes. Given a total of 5 groups."
        # ) as tracker:
        # self.play(Transform(text, text1), Transform(framebox0, framebox1), run_time=tracker.duration)
        self.play(Create(text2))
        self.play(Create(framebox2))
        self.wait(1)

        # self.play(FadeOut(text2))

        # with self.voiceover(
        #     text="notice, we also could further decompose the groups of sixes in two groups of threes."
        # ) as tracker:
        # self.play(Transform(text, text1), Transform(framebox0, framebox1), run_time=tracker.duration)
        self.play(Transform(text2, text3))
        self.play(Create(framebox3))
        self.play(FadeOut(framebox2))

        fcfdot = all_dots[0][0]
        fcldot = all_dots[0][len(list(all_dots[0])) - 1]
        lcfdot = all_dots[len(list(all_dots)) - 1][0]

        # X-axis
        line1 = Line(fcfdot.get_left(), fcldot.get_right()).shift([0, -0.5, 0])
        # b1 = Brace(line1)
        x_basis = len(list(all_dots[0]))
        t1 = Text(f"'X'-basis: {x_basis}", font_size=22).next_to(line1, DOWN)
        # self.play(Create(b2), Create(line2), Create(t))
        # b1_text = b1.get_text(f"'X'-basis: {x_basis}")

        # Y-axis
        line2 = Line(lcfdot.get_left(), fcfdot.get_left()).shift([-0.5, 0, 0])
        y_basis = len(list(all_dots))
        t2 = Text(f"'Y'-basis: {y_basis}", font_size=22).next_to(line2, LEFT)

        # with self.voiceover(
        #         text="This decomposition is final. We can't decompose any of the factors any further"
        # ) as tracker:
        self.play(Create(line1), Create(t1))
        self.play(Create(line2), Create(t2))

        # end
        self.wait(4)


class Decompose(Scene):
    def construct(self):
        n = 2**3 * 3**2
        all_dots = create_dots(3**2, 2**3, color=BLUE).center()
        text = Text(f"N = {n}", font_size=24).to_edge(UP).set_color(YELLOW)
        framebox0 = SurroundingRectangle(all_dots, buff=0.1)


# TwoDDots().render()
