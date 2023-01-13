import numpy as np
from wzk import mpl2
import axidraw

size = axidraw.dinA_inch[6]
pad = 0.03
line_height = 0.1
n_address_lines = 4
point_size = 12


def get_vert_line():
    vert = np.array([[pad, 2/3],
                     [1-pad, 2/3]])
    return [vert]


def get_address_lines():
    paths = []
    for i in range(n_address_lines):
        address2 = np.array([[1/2-line_height*i, 2/3+pad],
                             [1/2-line_height*i, 1-pad]])
        paths.append(address2)

    return paths


def get_address(name1, name2, street, city):
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


def read_stamp():
    directory = '/Users/jote/Documents/Code/Python/axidraw/data/svg'
    file = 'birds/bird_7.svg'
    drawing = axidraw.drawing.Drawing.load(f"{directory}/{file}")

    paths = axidraw.drawing.scale2(x=drawing.paths, size=size, padding=0.0, mi=0, ma=1, keep_aspect=False,
                                   center=False)

    # fig, ax = axidraw.drawing.new_fig(axidraw.dinA_inch[6])
    drawing.render()


def main():

    name1 = 'Lina Schmitz-Buhl'
    name2 = 'Sami Mahmoud'
    street = 'Zwinglistr. 24'
    city = '10555 Berlin'
    country = 'Deutschland'

    path_lines = get_address_lines()
    paths = axidraw.drawing.scale2(x=path_lines, size=size, padding=0.0, mi=0, ma=1, keep_aspect=False,
                                   center=False)
    path_text = get_address(name1=name1, name2=name2, street=street, city=city)

    drawing = axidraw.Drawing((axidraw.drawing.paths_wrapper(paths=paths) +
                               axidraw.drawing.paths_wrapper(paths=path_text)))

    # drawing = axidraw.Drawing(axidraw.drawing.paths_wrapper(paths=path_text))

    fig, ax = axidraw.drawing.new_fig(axidraw.dinA_inch[6])
    drawing.render(ax=ax)

    # drawing = drawing.sort_paths()
    axidraw.draw(drawing=drawing)

    # read_stamp()


# import svgpathtools as spt
#
# directory = '/Users/jote/Documents/Code/Python/axidraw/data/svg'
# file = 'birds/bird_25.svg'
#
# paths, attributes = spt.svg2paths(f"{directory}/{file}")
# n_steps = 1000
#
# paths2 = []
# for path in paths:
#     paths2.append(np.array([(path.point(i).real, path.point(i).imag) for i in np.linspace(start=0.0, stop=1.0, num=n_steps)]))
#
# spt.disvg(paths, stroke_widths=[0.1]*len(paths))
# fig, ax = mpl2.new_fig()
# for path in paths2:
#     ax.plot(*path.T, color='k', lw=1)


def draw_lines(font, lines, upper_left, lineheight, point_size, rotate=+90):
    font = axidraw.Font(font=axidraw.FUTURAL, point_size=point_size)

    path = []
    for i, line in enumerate(lines):
        y = upper_left[1]
        x = upper_left[0] - lineheight * i
        if line == '':
            continue
        path += __get_line(font=font, text=line, x=x, y=y, rotate=rotate)

    return path


rilke = ['Wunderliches Wort: die Zeit verteiben!',
         'Sie zu halten, waere das Problem.',
         'Denn, wen aengstigts nicht: wo ist ein Bleiben,',
         'wo ein endlich Sein in alledem? -',
         '',
         'Sieh, der Tag verlangsamt sich, entgegen',
         'jenem Raum, der ihn nach Abend nimmt:',
         'Aufstehen wurde Stehen, und Stehen wird legen,',
         'und das willig Liegende verschwimmt -',
         '',
         'Berge ruhn, von Sternen ueberpraechtigt; -',
         'aber auch in ihnen flimmert die Zeit.',
         'Ach, in meinem wilden Herzen naechtigt',
         'obdachlos die Unvergaenglichkeit.',
         '',
         '-Rainer Maria Rilke-']


from wzk import geometry

size_dinA6 = axidraw.dinA_inch[6]
size_dinA5 = axidraw.dinA_inch[5]
limits_dinA6 = np.array([[0.0, size_dinA6[0]],
                         [0.0, size_dinA6[1]]])
limits_dinA5 = np.array([[0.0, size_dinA5[0]],
                         [0.0, size_dinA5[1]]])


if __name__ == '__main__':
    pass
    # main()
    p = draw_lines(font=None, lines=rilke, upper_left=(axidraw.dinA_inch[5][1]-0.5, 0.3), lineheight=0.4, point_size=16)

    drawing = axidraw.Drawing(axidraw.drawing.paths_wrapper(paths=p))

    fig, ax = axidraw.drawing.new_fig(axidraw.dinA_inch[5])

    # drawing = axidraw.Drawing([geometry.box(limits_dinA5)])

    drawing.render(ax=ax)

    axidraw.draw(drawing=drawing)

