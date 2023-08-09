import numpy as np

import axidraw
from examples.mijorize import util


def get_step(x0, x1):
    x = np.zeros((4, 2))
    x[0] = [x0[0]*2, 0]
    x[1] = x0
    x[2] = [x0[0], x1[1]]
    x[3] = x1
    x = x[:, ::-1]
    return x


n = 29

x0 = np.array([np.linspace(start=0, stop=1, num=n), np.linspace(start=0, stop=1, num=n)]).T
x1 = x0 + 2 * 1/(n-1)


stair = np.array([get_step(xx0, xx1) for xx0, xx1 in zip(x0, x1)])

mi, ma = axidraw.drawing.get_min_max(stair)
x = axidraw.drawing.scale2(x=stair, size=axidraw.dinA_inch[6], padding=0.5, keep_aspect=True, center=True, mi=mi, ma=ma)
drawing = axidraw.Drawing(x)


drawing.render()
axidraw.draw(drawing=drawing)
util.draw_number("093")
