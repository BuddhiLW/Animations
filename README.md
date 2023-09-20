# Table of Contents

1.  [Installation](#orgd235b96)
    1.  [Instructions](#orgf9cc810)
        1.  [Create an environment with `Conda`](#org914b062)
        2.  [Activate the environment](#org986f6d3)
        3.  [Install dependencies](#org14d8f08)
    2.  [Summary](#org0d090ef)
2.  [Algorithm documentation (TODO)](#org9115a3f)
    1.  [Integrals and the Monte Carlo Method](#orgc2d2592)
    2.  [IFS](#org00a625f)
    3.  [Compound Interest and calculation of yearly, monthly and daily returns](#org9dd1f59)
    4.  [`Euclid's Algorithm`, the `Fundamental Arithmetic Theorem` and the `Decimal Number System`](#org31a053c)
        1.  [Animation - group of dots](#org4445006)
        2.  [Create Rounding Boxes](#org0dd49d2)

    (setq org-format-latex-options (plist-put org-format-latex-options :scale 3.0))


<a id="orgd235b96"></a>

# Installation

Instructions on creating, activating and download the dependencies will be given in `Instructions`

Prerequisites:

-   Conda
-   Manim
-   Numpy
-   Scipy


<a id="orgf9cc810"></a>

## Instructions


<a id="org914b062"></a>

### Create an environment with `Conda`

Let&rsquo;s create an environment, which we will call `manim`, but you can call it whatever you fell like.

    conda create -n manim python=3.11 anaconda


<a id="org986f6d3"></a>

### Activate the environment

In a terminal (for installing the dependencies), or (later on) in your favorite editor, activate the environment.

    conda activate manim

1.  Emacs

    In Emacs, you can use `M-x conda-env-activate`, using `conda.el` ([repository for conda.el](https://github.com/necaris/conda.el))
    
    Then, upon calling `run-python`, the python `repl` will be using conda&rsquo;s environment.
    
    Anything you sent to it, will contain the packages you installed (like manim). So, you can import it and run the animations.


<a id="org14d8f08"></a>

### Install dependencies

After activating the environment,

    conda install -c conda-forge manim numpy scipy


<a id="org0d090ef"></a>

## Summary

    conda create -n manim
    conda activate manim
    conda install -c conda-forge manim numpy scipy


<a id="org9115a3f"></a>

# TODO Algorithm documentation (TODO)


<a id="orgc2d2592"></a>

## Integrals and the Monte Carlo Method


<a id="org00a625f"></a>

## TODO IFS


<a id="org9dd1f59"></a>

## TODO Compound Interest and calculation of yearly, monthly and daily returns


<a id="org31a053c"></a>

## TODO `Euclid's Algorithm`, the `Fundamental Arithmetic Theorem` and the `Decimal Number System`

\begin{equation}
\begin{aligned}
\forall(x\,,y), \exists(t,r) \, \ni \, y = x*t + r
\end{aligned}
\end{equation}


<a id="org4445006"></a>

### Animation - group of dots

1.  Create `n` dots

    Given a number, create `n` dots, by using the greatest value, by one of the relative primes, which compose `n`.
    
        def create_n_dots(n, **kwargs):
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

2.  Create dots

    Given a number $p=n.m$, This function creates $n.m$ (2D-display) dots, in a `VGroup`.
    
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


<a id="org0dd49d2"></a>

### Create Rounding Boxes

1.  Create rounding box around `vgroups`

        def create_rouding_boxes(vgroups, *args, **kwargs):
            """VGroups"""
            color = kwargs["config"]["color"]
            text = kwargs["config"]["text"]
        
            if kwargs["config"].keys().__contains__("buff"):
                buff = kwargs["config"]["buff"]
            else:
                buff = 0.1
        
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

2.  Further decompose the rounding boxes

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

