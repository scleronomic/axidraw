import numpy as np
from wzk import mpl2, geometry, math2, spatial

import axidraw


x_fibonacci = geometry.fibonacci_sphere(n=74)
x_ball_fibonacci01 = x_fibonacci[:, [0, 1]]
x_ball_fibonacci12 = x_fibonacci[:, [1, 2]]

# mpl2.plot_projections_2d(x=x_fibonacci, marker='o', ls=None)


A = spatial.transform_2d.trans_theta2frame(trans=np.zeros(2), theta=np.deg2rad(-5))


def spiral(phi0=0, phi1=10*np.pi, r0=1.0, r1=0.0,
           r0y=None, r1y=None,
           n=10000):

    phi = np.linspace(phi0, phi1, n)

    if r0y is None:
        r0y = r0
    if r1y is None:
        r1y = r1

    rx = np.linspace(r0, r1, n)
    ry = np.linspace(r0y, r1y, n)

    x = np.cos(phi) * rx
    y = np.sin(phi) * ry

    return np.array([x, y]).T


def ellipse(rx, ry, n=1000):
    phi = np.linspace(0, np.pi*2, n)
    x = np.cos(phi) * rx
    y = np.sin(phi) * ry
    return np.array([x, y]).T


x_ball_spiral = spiral(n=10000)

# fig, ax = mpl2.new_fig(aspect=1)
# ax.plot(*x_ball_spiral.T, marker='o')

# x_ellipse = ellipse(rx=1, ry=3)
x_ellipse = spiral(phi1=28*2*np.pi, r0=5.5/2, r0y=7.5/2, n=10000)
x_line = np.array([[-0.15, -0.15, -0.075, -0.075, 0.0,  0.0,  0.075, 0.075,  0.15, 0.15],
                   [-3.75, -7,    -7,      -3.75, -3.75, -7, -7,     -3.75, -3.75, -7]]).T

x_ellipse = spatial.Ax(A, x_ellipse)
x_line = spatial.Ax(A, x_line)


# x_ball_spiral += np.array([[3, 0]])
x_ball_fibonacci01 += np.array([[+1.5, +1]])
# # x_ball_fibonacci12 += np.array([[+3, 0]])
# fig, ax = mpl2.new_fig(aspect=1)
# # ax.plot(*x_ball_fibonacci01.T, color="blue")
# ax.plot(*x_ball_fibonacci01.T, color="red")
# # ax.plot(*x_ball_spiral.T, color="red")
# ax.plot(*x_ellipse.T, color="black")
# ax.plot(*x_line.T, color="black")

limits = np.array([[-2.75, +2.75],
                   [-7, +3.75]])

x = axidraw.drawing.scale2(x=x_ball_fibonacci01, size=axidraw.dinA_inch[6], padding=0.5, keep_aspect=True, center=True,
                           mi=limits[:, 0], ma=limits[:, 1])
drawing = axidraw.Drawing(x)
axidraw.draw(drawing=drawing)

