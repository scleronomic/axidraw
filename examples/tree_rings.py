import math

from PIL import Image

import axidraw


def create_paths(im):
    f = (255 * 255 * 3) ** 0.5
    paths = []
    w, h = im.size
    print(h, w)
    for m in [-5, -3, -1, 0, 1, 3, 5]:

        for radius in range(0, w, 17):
            path = []
            for a in range(1800):
                a = math.radians(a / 10.0)
                x = w / 2 + int(math.cos(a) * radius)
                y = h - int(math.sin(a) * radius)
                if x < 0 or x >= w:
                    continue
                if y < 0 or y >= h:
                    continue
                r, g, b = im.getpixel((x, y))
                p = (r * r + g * g + b * b) ** 0.5
                p = 1 - (p / f)
                p = p ** 2
                if p < 0.05:
                    if len(path) > 1:
                        paths.append(path)
                    path = []
                else:
                    x = w / 2 + math.cos(a) * (radius + m * p * 1.5)
                    y = h - math.sin(a) * (radius + m * p * 1.5)
                    path.append((x, y))
            if len(path) > 1:
                paths.append(path)
    return paths


def main():
    file = "/Users/jote/Downloads/Sami/see.jpeg"
    paths = create_paths(Image.open(file))
    drawing = axidraw.Drawing(paths)
    drawing = drawing.sort_paths().join_paths(0.05)

    paths = axidraw.drawing.scale2(paths, size=axidraw.dinA_inch[5][::-1], padding=axidraw.cm2inch,
                                   center=False, keep_aspect=False)
    drawing = axidraw.Drawing(paths)
    fig, ax = axidraw.drawing.new_fig(axidraw.dinA_inch[5][::-1])

    drawing.render(ax=ax)

    # axidraw.draw(drawing)


if __name__ == "__main__":
    main()
