import numpy as np
from wzk.mpl2 import new_fig

import axidraw

pi = np.pi
n = 21
t = 4380

phi0 = np.linspace(0, t*np.pi, n) - 5/8*np.pi
phi1 = np.linspace(0, t*np.pi, n) - 1/8*np.pi
phi2 = np.linspace(0, t*np.pi, n) + np.pi/2
r = np.linspace(1, 0.3, n).repeat(3)

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

drawing = axidraw.Drawing(x)
drawing.render()
# input()
axidraw.draw(drawing=drawing)
