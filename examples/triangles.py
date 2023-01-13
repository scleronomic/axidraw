import numpy as np
from wzk.mpl2 import new_fig

import axidraw

pi = np.pi
n = 100

t = 111111111
phi0 = np.linspace(0, t*np.pi, n) - 5/6*np.pi
phi1 = np.linspace(0, t*np.pi, n) - 1/6*np.pi
phi2 = np.linspace(0, t*np.pi, n) + np.pi/2
r = np.linspace(1, 0.01, n).repeat(3)

phi = np.zeros(3*n)
phi[::3] = phi0
phi[1::3] = phi1
phi[2::3] = phi2
phi = phi[::-1]
phi0 = phi0[::-1]
phi1 = phi1[::-1]
phi2 = phi2[::-1]
x = np.array((np.cos(phi), np.sin(phi))).T * r[:, np.newaxis]


x = axidraw.drawing.scale2(x=x, size=axidraw.dinA_inch[6], padding=0.5, keep_aspect=True, center=True)
fig, ax = new_fig(aspect=1)
ax.set_xlim(0, axidraw.dinA_inch[6][0])
ax.set_ylim(0, axidraw.dinA_inch[6][1])
ax.plot(*x.T, color='black')


drawing = axidraw.Drawing([x])
# axidraw.draw(drawing=drawing)
