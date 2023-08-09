import numpy as np
from wzk import perlin, trajectory


def get_wobbly_line(n=1000, scale=2.0, mi=None, ma=None):
    r = perlin.perlin_noise_1d(n=n, m=20, scale=1)
    r += -r.min() + 1
    above = r > r[0]
    try:
        i_above = np.nonzero(np.diff(above))[0][-1]
    except IndexError:
        return get_wobbly_line(n=n, scale=scale)
    r = r[:i_above+1]
    r[-1] = r[0]

    r = trajectory.get_path_adjusted(x=r[:, np.newaxis], n=n, enforce_equal_steps=True)[:, 0]
    r = np.roll(r, shift=np.random.randint(low=0, high=n))
    if mi is not None and ma is not None:
        s = ma - mi
        r -= np.min(r)
        r /= np.max(r)
        r = mi + s * r
    return r


def wobbly_circle(n=1000, scale=2.0, mi=None, ma=None):
    phi = np.linspace(start=0, stop=2*np.pi, num=n)
    r = get_wobbly_line(n=n, mi=mi, ma=ma)
    x = np.vstack([np.cos(phi), np.sin(phi)]) * r
    return x.T


def line_transition(l0, l1, n):
    dl = l1 - l0
    n = n - 1
    lines = []
    for i in range(n):
        lines.append(l0 + i/n * dl)
    lines.append(l1)
    return lines
