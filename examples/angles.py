import numpy as np

from wzk import mpl2
import axidraw


BOUNDS = axidraw.dinA_inch[3]
RADIUS = 4
STEP = 5


def main():
    w, h = BOUNDS[-2:]
    paths = []
    r = RADIUS
    for a in range(0, 180, STEP):
        a = np.deg2rad(a)
        c = np.cos(a)
        s = np.sin(a)
        paths.append([(-r * c, -r * s), (r * c, r * s)])
    d = axidraw.Drawing(paths)
    d = d.center(w, h)
    d = d.sort_paths()
    d.render(bounds=BOUNDS)


if __name__ == '__main__':
    main()



