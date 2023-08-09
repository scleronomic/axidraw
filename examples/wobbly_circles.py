import numpy as np
from wzk import perlin, mpl2, math2, geometry, trajectory





n_circle = 1000
n_radius = 1000

# for i in range(10):
#     fig, ax = mpl2.new_fig(aspect=1)
#     xx = wobbly_circle(n=n_circle)
#     ax.plot(*xx.T)

fig, ax = mpl2.new_fig(aspect=1)
inner_circle = wobbly_circle(n=n_circle, mi=0.01, ma=0.1) * 0.1
outer_circle = wobbly_circle(n=n_circle, mi=1, ma=1.05) * 2


def abs_log(x):
    x[x > 0] = np.log(x[x > 0])
    x[x < 0] = -np.log(-x[x < 0])
    return x

# outer_circle = abs_log(outer_circle)
# inner_circle = abs_log(inner_circle)

r0 = perlin.perlin_noise_1d(n=n_radius, m=8, scale=1)
r1 = perlin.perlin_noise_1d(n=n_radius, m=8, scale=1)
r2 = perlin.perlin_noise_1d(n=n_radius, m=8, scale=1)
# r0[:] = 1



ra = get_line_transition(r0, r1, n=333)
rb = get_line_transition(r1, r2, n=333)
rc = get_line_transition(r2, r0, n=333)
rr = ra + rb + rc
# fig, ax = mpl2.new_fig()
# for i in range(0, n_circle, 20):
#     ax.plot(rr[i]+i*0.1)


for i in range(0, n_circle, 5):

    x_radius = np.linspace(start=inner_circle[i, 0], stop=outer_circle[i, 0], num=n_radius)
    y_radius = np.linspace(start=inner_circle[i, 1], stop=outer_circle[i, 1], num=n_radius)
    x_r = np.vstack([x_radius, y_radius]).T
    x_r_n = x_r[-1] / np.linalg.norm(x_r)
    x_o = geometry.get_ortho_star_2d(x_r_n)[1]

    x_ro = x_r + rr[i][:, np.newaxis] * x_o[np.newaxis, :]
    # ax.plot([0, xx[i, 0]], [0, xx[i, 1]], color="black")
    ax.plot(*x_ro.T, color="black")




def perlin_1d_transition(n):
    r0 = perlin.perlin_noise_1d(n=n, m=4, scale=1)
    r1 = perlin.perlin_noise_1d(n=n, m=4, scale=1)

    dr = r1 - r0

    fig, ax = mpl2.new_fig()
    m = 10
    for i in range(m):
        ax.plot(r0 + i*dr/m + i, color="black")
    ax.plot(r0, color="red")
    ax.plot(r1 + 10, color="blue")



