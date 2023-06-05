import numpy as np
import axidraw


def get_vert_line(pad):
    vert = np.array([[pad, 2/3],
                     [1-pad, 2/3]])
    return [vert]


def get_address_lines(n, height, pad):
    paths = []
    for i in range(n):
        address2 = np.array([[1/2-height*i, 2/3+pad],
                             [1/2-height*i, 1-pad]])
        paths.append(address2)

    return paths


def get_address(name1, name2, street, city,
                pad, point_size, size, line_height):
    font = axidraw.Font(font=axidraw.FUTURAL, point_size=point_size)
    dy = (2 / 3 + pad) * axidraw.dinA_inch[6][1]
    dx0 = 2.2
    path = []
    path += __get_line(font=font, text=name1, x=dx0, y=dy)
    path += __get_line(font=font, text=name2, x=dx0 - 1 * line_height*size[0], y=dy)
    path += __get_line(font=font, text=street, x=dx0 - 2 * line_height*size[0], y=dy)
    path += __get_line(font=font, text=city, x=dx0 - 3 * line_height*size[0], y=dy)

    return path


def __get_line(font, text, x, y, rotate=+90):
    d = font.wrap(t=text, width=10, line_spacing=1.5, justify=True)
    d = d.rotate(rotate)
    d = d.translate(dx=x, dy=y)
    return d.paths


def draw_lines(font, lines, upper_left, lineheight, point_size, rotate=+90):
    font = axidraw.Font(font=axidraw.FUTURAL, point_size=point_size)

    path = []
    for i, line in enumerate(lines):
        y = upper_left[1] - lineheight * i
        x = upper_left[0]  #  - lineheight * i  # TODO
        if line == '':
            continue
        path += __get_line(font=font, text=line, x=x, y=y, rotate=rotate)

    return path