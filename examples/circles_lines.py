import numpy as np
from wzk.mpl import new_fig


pi = np.pi

n = 72
delta0 = np.pi / 72
delta1 = np.pi / 36

phi0 = np.linspace(0, 2*np.pi, n)
phi1 = np.linspace(0, 4*np.pi, n)

phi = np.zeros(4*n)
phi[::4] = phi0
phi[1::4] = phi0 + delta0
phi[2::4] = phi1
phi[3::4] = phi1 + delta1

phi = np.clip(phi, 0, 2*np.pi)

x = np.cos(phi)
y = np.sin(phi)

fig, ax = new_fig(aspect=1)
fig.set_size_inches((10, 10))
ax.set_axis_off()

phi_u = np.unique(phi)
x = np.concatenate([x, np.cos(phi_u)])
y = np.concatenate([y, np.sin(phi_u)])
x = np.array((x, y)).T




import axidraw
x = axidraw.drawing.scale2(x=x, size=axidraw.dinA_inch[3], padding=2, keep_aspect=False)


fig, ax = new_fig(aspect=1)
ax.set_xlim(0, axidraw.dinA_inch[3][0])
ax.set_ylim(0, axidraw.dinA_inch[3][1])
ax.plot(*x.T, color='black')

path = [(xx[0], xx[1]) for xx in x]
drawing = axidraw.Drawing([path])
axidraw.draw(drawing=drawing)


# path = np.array(drawing.paths[0])
# fig, ax = new_fig(aspect=1)
# ax.plot(*path.T, color='black')

