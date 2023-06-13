import numpy as np
from wzk import perlin, mpl2, math2, geometry


def wobbly_circle(n=1000, scale=2.0):
    phi = np.linspace(start=0, stop=2*np.pi, num=n)
    r = perlin.perlin_noise_1d(n=n, m=4, scale=1)
    print(r.min())
    r += 2
    x = np.vstack([np.cos(phi), np.sin(phi)]) * r
    return x.T


n_circle = 1000
n_radius = 1000
r0 = perlin.perlin_noise_1d(n=n_radius, m=4, scale=1)
fig, ax = mpl2.new_fig(aspect=1)
xx = wobbly_circle(n=n_circle)
ax.plot(*xx.T)
for i in range(0, n_circle, 20):

    x_radius = np.linspace(0, xx[i, 0], n_radius)
    y_radius = np.linspace(0, xx[i, 1], n_radius)
    x_r = np.vstack([x_radius, y_radius]).T
    x_r_n = x_r[-1] / np.linalg.norm(x_r)
    x_o = geometry.get_ortho_star_2d(x_r_n)[1]

    x_ro = x_r + r0[:, np.newaxis] * x_o[np.newaxis, :]
    # ax.plot([0, xx[i, 0]], [0, xx[i, 1]], color="black")
    ax.plot(*x_ro.T, color="black")


def perlin_1d_transition(n):
    r0 = perlin.perlin_noise_1d(n=n, m=4, scale=1)
    r1 = perlin.perlin_noise_1d(n=n, m=4, scale=1)

    dr = r1 - r0
    dr = dr

    fig, ax = mpl2.new_fig()
    m = 10
    for i in range(m):
        ax.plot(r0 + i*dr/m + i, color="black")
    ax.plot(r0, color="red")
    ax.plot(r1 + 10, color="blue")

