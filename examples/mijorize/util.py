import axidraw
from axidraw import lines


def draw_number(n):
    number = lines.draw_lines(font=None, lines=[n], upper_left=(3.8, 5.3), lineheight=0.3, point_size=16, rotate=90)
    drawing = axidraw.Drawing(number)
    axidraw.draw(drawing=drawing)
