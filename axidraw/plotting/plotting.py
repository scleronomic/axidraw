import numpy as np
from wzk import perlin, trajectory, geometry, np2, mpl2

import axidraw


def make_ends_meet(x, mode):

    n = len(x)

    if mode is None:
        pass

    elif mode == "cut":
        above = x > x[0]
        try:
            i_above = np.nonzero(np.diff(above))[0][-1]
        except IndexError:
            return make_ends_meet(x=x, mode=mode)
        x = x[:i_above + 1]
        x[-1] = x[0]
        x = trajectory.get_path_adjusted(x=x[:, np.newaxis], n=n, enforce_equal_steps=True)[:, 0]

    elif mode == "linear-shift":
        dx = np.linspace(0, x[0] - x[-1], n)
        x = x + dx

    else:
        raise ValueError("mode must be 'cut' or 'linear-shift'")

    return x


def get_wobbly_line(n=1000,
                    m=20,
                    scale=1,
                    meet_ends=None, shift=False, mi=None, ma=None, x0=None):
    x = perlin.perlin_noise_1d(n=n, m=m, scale=scale)
    x += -x.min() + 1

    x = make_ends_meet(x=x, mode=meet_ends)
    if shift:
        x = np.roll(x, shift=np.random.randint(low=0, high=n))

    if mi is not None and ma is not None:
        s = ma - mi
        x -= np.min(x)
        x /= np.max(x)
        x = mi + s * x

    if x0 is not None:
        x = x - x[0] + x0
    return x


def wobbly_circle(n=1000, scale=2.0, mi=None, ma=None):
    phi = np.linspace(start=0, stop=2*np.pi, num=n)
    r = get_wobbly_line(n=n, mi=mi, ma=ma)
    x = np.vstack([np.cos(phi), np.sin(phi)]) * r
    return x.T


def line_transition(lines, n):

    if len(lines) == 2:
        l0, l1 = lines
        dl = l1 - l0
        n = n - 1
        lines2 = []
        for i in range(n):
            lines2.append(l0 + i/n * dl)
        lines2.append(l1)
        return np.array(lines2)

    else:
        lines2 = []
        m = n // (len(lines) - 1) + 1
        for i in range(len(lines) - 1):
            lines2.append(line_transition(lines[i:i+2], n=m)[:-1])

        return np.array(lines2).reshape((len(lines) - 1) * (m-1), len(lines[0]))


def radial_transition(c0, c1, r, n):
    circles = []

    for i in range(n):
        x_radius = np.linspace(start=c0[i, 0], stop=c1[i, 0], num=len(r))
        y_radius = np.linspace(start=c0[i, 1], stop=c1[i, 1], num=len(r))
        x_r = np.vstack([x_radius, y_radius]).T
        x_r_n = x_r[-1] / np.linalg.norm(x_r)
        x_o = geometry.get_ortho_star_2d(x_r_n)[1]

        x_ro = x_r + r[i][:, np.newaxis] * x_o[np.newaxis, :]

        circles.append(x_ro[::3][::-1])

    return np.array(circles)


def clip2limits(paths, limits):
    paths2 = []
    for i, p in enumerate(paths):
        p = np.array(p)

        above_lower = p >= limits[:, 0]
        below_lower = ~above_lower
        below_upper = p <= limits[:, 1]
        above_upper = ~below_upper
        if np.all(above_lower) and np.all(below_upper):  # all points are within limits
            paths2.append(p)
        elif np.logical_or(below_lower, above_upper).all():  # all points are outside limits
            continue
        else:  # some points are within limits
            b = np.logical_and(above_lower, below_upper).sum(axis=-1) == 2
            j = np2.get_interval_indices(b)
            for jj in j:
                paths2.append(p[jj[0]:jj[1]])

    return paths2


def translate(paths, offset):
    paths2 = []
    for p in paths:
        p = np.array(p)
        paths2.append(p + offset)
    return paths2


def get_part(x, i, j, size_element, size_total):

    e0 = np.array([[1], [0]])
    e1 = np.array([[0], [1]])

    d0 = (size_element[0] - 1 * axidraw.cm2inch)
    d1 = (size_element[1] - 1 * axidraw.cm2inch)

    limits_element = np.zeros((2, 2))
    limits_element[:, 1] = size_element
    limits_ij = limits_element + i * e0 * d0 + j * e1 * d1

    limits_clip = limits_ij.copy()
    limits_clip[:, 0] += 1 / 2 * axidraw.cm2inch

    x_ij = clip2limits(x, limits_clip)
    fig, ax = axidraw.drawing.new_fig(size_total)
    # plot_paths(ax=ax, paths=x, color='k', lw=0.1)
    mpl2.plot_box(ax=ax, limits=limits_ij, color='r', lw=0.5)
    x_ij = translate(x_ij, offset=-np.array([i * d0, j * d1]))

    return x_ij
