from manim import *
import numpy as np
from scipy.optimize import fsolve

# from scipy.optimize import fsolve
from sympy import *
import sympy.abc as abc

# from sympy import solve
# from sympy.abc import x, y, z


class ExampleCone(ThreeDScene):
    def cross(self, u, v):
        return np.cross(u, v) / np.linalg.norm(np.cross(u, v))

    def plane(self, x, y, u=[1, 0, 0], v=[0, 1, 0], x0=[0, 0, 0]):
        n = self.cross(u, v)
        d = np.dot(n, x0)
        if n[2] == 0:
            z = np.inf
        else:
            z = (d - n[0] * x - n[1] * y) / n[2]

        return np.array([x, y, z])

    def cone(self, x, y, x0=[0, 0, 0]):
        x = x - x0[0]
        y = y - x0[1]
        z = np.sqrt(x**2 + y**2) - x0[2]
        return np.array([x, y, z])

    def plane_cone_intersection(self, u, v, x0_plane, x0_cone):
        x, y, z = symbols("x, y, z")
        n = self.cross(u, v)
        # Plane equation
        eq1 = Eq(
            n[0] * (x - x0_plane[0])
            + n[1] * (y - x0_plane[1])
            + n[2] * (z - x0_plane[2]),
            0,
        )
        # Cone equation
        eq2 = Eq((x - x0_cone[0]) ** 2 + (y - x0_cone[1]) ** 2 - (z - x0_cone[2]), 0)

        def func(x, y, z):
            return [
                (
                    n[0] * (x - x0_plane[0])
                    + n[1] * (y - x0_plane[1])
                    + n[2] * (z - x0_plane[2]),
                    0,
                ),
                ((x - x0_cone[0]) ** 2 + (y - x0_cone[1]) ** 2 - (z - x0_cone[2]), 0),
            ]

        scipy_sol = lambda x, y, z: fsolve(func, [x, y, z])
        return solve([eq1, eq2], [x, y, z], dict=True), scipy_sol_func

    def construct(self):
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=7 * PI / 16, theta=PI / 3)
        self.add(axes)
        u0, v0, x0_plane = [1, 0, 0], [0, 1, 0], [1, 1, 1]
        x0_cone = [1, 1, 0]

        cone = Surface(
            lambda x, y: axes.c2p(*self.cone(x, y, x0=x0_cone)),
            u_range=[-5, 5],
            v_range=[-5, 5],
            resolution=8,
        )

        plane = Surface(
            lambda x, y: axes.c2p(*self.plane(x, y, u=u0, v=v0, x0=x0_plane)),
            u_range=[-5, 5],
            v_range=[-5, 5],
            resolution=8,
        )

        print(self.plane_cone_intersection(u0, v0, x0_plane, x0_cone))
        intersection_solution = self.plane_cone_intersection(u0, v0, x0_plane, x0_cone)
        # roots_x = [float(s) for s in solve(intersection_solution[0][abc.x])]
        intersection_graph = axes.plot_parametric_curve(
            lambda t: np.array(
                [
                    lambdify([abc.y], intersection_solution[0][abc.x])(t),
                    # np.sin(t),
                    t,
                    # np.cos(t),
                    lambdify([abc.y], intersection_solution[0][abc.z])(t),
                ]
            ),
            t_range=[-3, 3],
            # t_range=[float(roots_x[0]), float(roots_x[1])],
            color=RED,
        )
        self.play(Create(intersection_graph))

        # graph = ParametricSurface(
        #     lambda x, y: (
        #         axes.c2p(*intersection_solution[0][x], y, *intersection_solution[0][z])
        #     ),
        #     u_range=[0, 1],
        #     v_range=[0, 1],
        #     resolution=8,
        # )

        self.add(cone, plane)
        # self.add(graph)
        self.wait(2)


ExampleCone().render()
