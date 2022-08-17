import numpy as np
from wzk.mpl import new_fig


pi = np.pi

n = 3

phi0 = np.linspace(0, 2*np.pi, n) - 5/6*np.pi
phi1 = np.linspace(0, 2*np.pi, n) - 1/6*np.pi
phi2 = np.linspace(0, 2*np.pi, n) + np.pi/2
r = np.linspace(1, 0.9, n).repeat(3)

phi = np.zeros(3*n)
phi[::3] = phi0
phi[1::3] = phi1
phi[2::3] = phi2
phi = phi[::-1]
phi0 = phi0[::-1]
phi1 = phi1[::-1]
phi2 = phi2[::-1]
x = np.array((np.cos(phi), np.sin(phi))).T * r[:, np.newaxis]

phi = np.linspace(0, 2*np.pi, n)


def scale2(x, size, padding, keep_aspect=True):
    size, padding = np.atleast_1d(size, padding)
    scale = np.ones(2) * (size - 2*padding)

    x -= x.min(axis=0)
    scale = (scale / x.max(axis=0))
    if keep_aspect:
        scale = scale.min()
    x *= scale
    x += padding
    return x


x = scale2(x=x, size=(4, 4), padding=1)
fig, ax = new_fig(aspect=1)
ax.set_xlim(0, 8.3)
ax.set_ylim(0, 11.7)
ax.plot(*x.T, color='black')


path = [(xx[0], xx[1]) for xx in x]
import axidraw
drawing = axidraw.Drawing([path])
axidraw.draw(drawing=drawing)

