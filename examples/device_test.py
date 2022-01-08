import numpy as np
import axidraw


def circle(cx, cy, r, n):
    phi = np.linspace(0, 2*np.pi, n)
    x = cx + np.cos(phi) * r
    y = cy + np.sin(phi) * r
    points = np.array((x, y)).T
    return points


def main():
    path = []
    for i in range(10):
        path.append(circle(4, 4, (i + 1) * 0.2, 3600))
    drawing = axidraw.Drawing([path]).simplify_paths(0.001)
    drawing.render()
    # axidraw.draw(drawing)


if __name__ == '__main__':
    main()
