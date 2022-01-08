import axidraw
import math

BOUNDS = axidraw.A3_BOUNDS
RADIUS = 4
STEP = 5


def main():
    w, h = BOUNDS[-2:]
    paths = []
    r = RADIUS
    for a in range(0, 180, STEP):
        a = math.radians(a)
        c = math.cos(a)
        s = math.sin(a)
        paths.append([(-r * c, -r * s), (r * c, r * s)])
    d = axidraw.Drawing(paths)
    d = d.center(w, h)
    d = d.sort_paths()
    d.render(bounds=BOUNDS)


if __name__ == '__main__':
    main()
