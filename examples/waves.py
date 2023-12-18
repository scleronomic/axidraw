import random
import numpy as np
from wzk import mpl2, np2, spatial, geometry

from collections import defaultdict
from math import pi, sin, cos, hypot, floor
from shapely.geometry import LineString
import axidraw

amplitude = 0.012
frequency = 30
offset = amplitude*1.25
n = 1000
x0 = np.linspace(-1, 1, 1000)
y0 = amplitude * np.sin(frequency*x0)
xy0 = np.array([x0, y0]).T


def truncate_and_add(paths, xy):
    d = np.linalg.norm(xy, axis=1)
    j = np2.get_interval_indices(d < 1)
    for j0, j1 in j:
        xxyy = xy[j0:j1]
        print(np.max(xxyy))
        print(np.min(xxyy))

        paths.append(xy[j0:j1])
    return paths


def full(n):
    paths = []
    for i in range(n):
        xy = np.array([x0, y0-1-amplitude+i*offset]).T
        paths = truncate_and_add(paths, xy)

        if np.all(xy[:, 1] > 1):
            break

    return paths


def circle():
    paths = []
    n_rays = 100
    r = 0.37
    xy1 = np.array([x0+1, y0]).T

    phi_list = np.linspace(-np.pi / 4, +3 / 4 * np.pi, num=n_rays)
    theta_list = np.linspace(0, +np.pi, num=n_rays)
    for phi, theta in zip(phi_list, theta_list):

        trans = r*np.array([np.cos(phi), np.sin(phi)])  # np.array([-1, 0]) +
        A = spatial.twod.trans_theta2frame(trans=trans, theta=theta)

        xy = spatial.Ax(A=A, x=xy1)

        paths = truncate_and_add(paths, xy)

    return paths

paths0 = full(50)
paths1 = circle()
paths = paths0 + paths1

# fig, ax = mpl2.new_fig(aspect=1)
# for xy in paths:
#     ax.plot(*xy.T, color="black")
#     mpl2.plt.pause(0.1)
#
#

size = np.array([12, 18])*axidraw.cm2inch
print(size)
print(axidraw.dinA_inch[6])
x = axidraw.drawing.scale2(paths, size=size,
                           padding=axidraw.cm2inch/2, mi=-1, ma=1, center=True, keep_aspect=True)

fig, ax = axidraw.drawing.new_fig(size)
axidraw.drawing.plot_paths(ax=ax, paths=x, color='k', lw=0.1)

# x = [geometry.box(axidraw.limits_dinA[5])]
drawing = axidraw.Drawing(x)
# drawing = drawing.sort_paths()
drawing.render()
# axidraw.draw(drawing=drawing)