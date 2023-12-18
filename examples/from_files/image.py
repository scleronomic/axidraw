import numpy as np
from wzk import mpl2
import axidraw

size = axidraw.dinA_inch[6]
pad = 0.03
line_height = 0.1
n_address_lines = 4
point_size = 12


directory = '/Users/jote/Documents/code/python/misc/axidraw/data/svg'
file = 'one-piece/gum-gum-fruit.svg'
# file = 'birds/bird_0.svg'

from xml.dom import minidom

doc = minidom.parse(f"{directory}/{file}")  # parseString also exists
path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
doc.unlink()



drawing = axidraw.drawing.Drawing.load(f"{directory}/{file}")

drawing = axidraw.drawing.scale2(x=drawing.paths, size=size, padding=0.0, mi=0, ma=1, keep_aspect=False,
                               center=False)
drawing = axidraw.Drawing(drawing)
drawing.render()


from svg.path import parse_path
from svg.path.path import Line
from xml.dom import minidom

# read the SVG file
doc = minidom.parse(f"{directory}/{file}")
path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
doc.unlink()

# print the line draw commands
for path_string in path_strings:
    path = parse_path(path_string)
    for e in path:
        if isinstance(e, Line):
            x0 = e.start.real
            y0 = e.start.imag
            x1 = e.end.real
            y1 = e.end.imag
            print("(%.2f, %.2f) - (%.2f, %.2f)" % (x0, y0, x1, y1))



from svgpathtools import svg2paths
paths, attributes = svg2paths(f"{directory}/{file}")

for k, v in enumerate(attributes):
    print(v['d'])  # print d-string of k-th path in SVG