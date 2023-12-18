import numpy as np
import axidraw


n = 1000
seed = 2
np.random.seed(2)

line1 = axidraw.plotting.get_wobbly_line(n=n, m=8, meet_ends="linear-shift", mi=-2, ma=+2, x0=0)
line2 = axidraw.plotting.get_wobbly_line(n=n, m=20, meet_ends="linear-shift", mi=-0.4, ma=+0.4, x0=0)
line3 = axidraw.plotting.get_wobbly_line(n=n, m=8, meet_ends="linear-shift", mi=-2, ma=+2, x0=0)
rr = axidraw.plotting.line_transition(lines=[line1, line2, line3], n=50)

x = [np.array([np.linspace(0, 1, n), rrr+i*0.1]) for (i, rrr) in enumerate(rr)]
x = np.array(x).transpose((0, 2, 1))
x = x[:, :, ::-1]


x = axidraw.drawing.scale2(x, size=axidraw.dinA_inch[6], padding=2*axidraw.cm2inch, center=True,
                           keep_aspect=False)

drawing = axidraw.Drawing(x)
# drawing.render(title=str(seed))
# drawing = drawing.sort_paths()

axidraw.draw(drawing)