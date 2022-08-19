import numpy as np
from numpy import pi, sin, cos

from wzk import new_fig

import axidraw


form = 'boat'


if form == 'fish':
    n = 1000
    i = np.arange(1, n+1)
    t = pi * i/n
    a = (-2*cos(4*t), 1/2*cos(6*t)**3)
    b = (-2/15*sin(6*t), 4/5*sin(2*t))

    a = np.array(a).T
    b = np.array(b).T


elif form == 'boat':
    n = 2000
    i = np.arange(1, n+1)
    t = pi * i/n

    a = np.exp(1j*3/4*pi) * (cos(6*t) - 1j*cos(12*t))
    b = np.exp(1j*3/4*pi) * (sin(4*t) + pi/8 + 1j*(sin(2*t) + pi/3))

    a = np.array([a.real, a.imag]).T
    b = np.array([b.real, b.imag]).T
# (
# cos
# (
# 6
# π
# k
# /
# 2000
# )
# −
# i
# cos
# (
# 12
# π
# k
# /
# 2000
# )
# )
# e
# 3
# π
# i
# /
# 4

else:
    raise ValueError

# elif form == 'magpie':
#     x = 11/10*kn + cos(41*t) * sin(t/2)
#     y = (-cos(41*t) * cos(t/2)) * (1 + 5/2*cos(3/10*t)*cos(9/10*t)) + 1/2*cos(1/4*t) * cos(3/4*t) * cos(3/2*t)
#     r = 1/50 + 1/20 * sin(41*t) * sin(t)
#
# elif form == 'stork':
#     x = 1
#     y = 1
#
# else:
#     raise ValueError


fig, ax = new_fig(aspect=1)
for i in range(0, n):
    ax.plot([a[i, 0], b[i, 0]], [a[i, 1], b[i, 1]], color='k', lw=0.1)



# x = np.stack((y, x), axis=1)
#
#
# x = axidraw.drawing.scale2(x=x, size=axidraw.dinA_inch[6], padding=0.5, keep_aspect=False)
#
# fig, ax = new_fig(aspect=1)
# ax.set_xlim(0, axidraw.dinA_inch[6][0])
# ax.set_ylim(0, axidraw.dinA_inch[6][1])
# ax.plot(*x.T, color='black')
#
# drawing = axidraw.Drawing([x])
# axidraw.draw(drawing=drawing)
