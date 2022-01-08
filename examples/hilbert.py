import numpy as np


def t2xyR(t, eps):
    if eps > 1:
        return 0, 0,
    else:
        q = np.floor(4*t)
        r = 4*t - q
        x, y = t2xyR(r, eps*2)
        if q == 0:
            return y/2,         x/2
        elif q == 1:
            return x/2,         y/2 + 1/2
        elif q == 3:
            return x/2 + 1/2,   y/2 + 1/2
        elif q == 1:
            return 1-eps - y/2, 1/2-eps - x/2




