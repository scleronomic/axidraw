import numpy as np
from wzk.mpl import new_fig


def d_lorenz(x, y, z, s=10, r=28, b=2.667):
    """
    Given:
       x, y, z: a point of interest in three dimensional space
       s, r, b: parameters defining the lorenz attractor
    Returns:
       x_dot, y_dot, z_dot: values of the lorenz attractor's partial
           derivatives at the point x, y, z
    """
    x_dot = s*(y - x)
    y_dot = r*x - y - x*z
    z_dot = x*y - b*z
    return x_dot, y_dot, z_dot


def solve_lorenz(dt=0.001, t=100):

    num_steps = int(t // dt)

    xs = np.empty(num_steps + 1)
    ys = np.empty(num_steps + 1)
    zs = np.empty(num_steps + 1)

    xs[0], ys[0], zs[0] = (0., 1., 1.05)

    for i in range(num_steps):
        x_dot, y_dot, z_dot = d_lorenz(xs[i], ys[i], zs[i])
        xs[i + 1] = xs[i] + (x_dot * dt)
        ys[i + 1] = ys[i] + (y_dot * dt)
        zs[i + 1] = zs[i] + (z_dot * dt)

    return xs, ys, zs


xs, ys, zs = solve_lorenz(dt=0.001, t=100)


x = np.array(((xs+ys) / 1.5, zs)).T



import axidraw

x = axidraw.drawing.scale2(x, size=axidraw.A3_SIZE, padding=1, keep_aspect=False)

# fig, ax = new_fig(aspect=1)
# ax.set_xlim(0, axidraw.A3_SIZE[0])
# ax.set_ylim(0, axidraw.A3_SIZE[1])
# ax.plot(*x.T, lw=0.5, color='black')


path = [(xx[0], xx[1]) for xx in x]
drawing = axidraw.Drawing([path])
axidraw.draw(drawing=drawing)
