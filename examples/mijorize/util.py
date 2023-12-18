import axidraw
from axidraw import lines, dinA_inch


def draw_number(n, dinA, rotate=90, point_size=16):
    number = lines.draw_lines(font=None, lines=[n], upper_left=(3.8, 5.3), lineheight=0.3, point_size=point_size, rotate=rotate)
    drawing = axidraw.Drawing(number)
    axidraw.draw(drawing=drawing)
