import numpy as np
from numpy import pi, sin, cos

from wzk import new_fig

import axidraw


n = 10000
k = np.arange(-n, n)
kn = k/n
t = kn * pi
bird = 'parrot'


if bird == 'original':
    x = ((3/2*kn) + sin(pi/2*kn**7) * cos(41*t)**6 +
         1/4*cos(41*t)**16 * cos(t/2)**12 * sin(6*t))
    y = (-cos(pi/2*kn**7) * (1 + 3/2 * cos(t/2)**6 * cos(3/2*t)**6) * cos(41*t)**6 +
         1/2 * cos(3/10*t)**10 * cos(9/10*t)**10 * cos(18/10*t)**10)
    r = (1/50 + 1/10*sin(41*t)**2 * sin(9/10*t)**2 +
         1/20*cos(41*t)**2 * cos(t/2)**10)
    y = y+r

elif bird == 'parrot':
    x = (3 / 2 * kn + cos(37 * t) ** 6 * sin(3 / 5 * pi * kn ** 7) +
         9 / 7 * cos(37 * t) ** 16 * cos(t / 2) ** 12 * sin(t))
    y = (-5 / 4 * cos(37 * t) ** 6 * cos(3 / 5 * pi * kn ** 7) * (1 + 3 * (cos(t / 2) * cos(3 / 2 * t)) ** 8) +
         2 / 3 * cos(3 / 20 * t) * cos(9 / 20 * t) * cos(9 / 10 * t) ** 12)
    r = 0

elif bird == 'magpie':
    x = 11/10*kn + cos(41*t) * sin(t/2)
    y = (-cos(41*t) * cos(t/2)) * (1 + 5/2*cos(3/10*t)*cos(9/10*t)) + 1/2*cos(1/4*t) * cos(3/4*t) * cos(3/2*t)
    r = 1/50 + 1/20 * sin(41*t) * sin(t)

elif bird == 'stork':
    x = 1
    y = 1

else:
    raise ValueError

x = np.stack((y, x), axis=1)


x = axidraw.drawing.scale2(x=x, size=axidraw.dinA_inch[6], padding=0.5, keep_aspect=False)

fig, ax = new_fig(aspect=1)
ax.set_xlim(0, axidraw.dinA_inch[6][0])
ax.set_ylim(0, axidraw.dinA_inch[6][1])
ax.plot(*x.T, color='black')
#
drawing = axidraw.Drawing([x])
axidraw.draw(drawing=drawing)
