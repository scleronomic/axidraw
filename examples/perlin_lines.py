import numpy as np
import axidraw
from wzk import geometry, perlin, mpl2
from examples.mijorize import util


n = 500
n_radius = 1000

n_years = 28
np.random.seed(28)
r = [axidraw.plotting.get_wobbly_line(n=n, m=10+i, meet_ends="linear-shift", mi=-1, ma=+1, x0=0) for i in range(n_years+1)]
rr = axidraw.plotting.line_transition(lines=r, n=n_years*12)

x = [np.array([np.linspace(0, 1, n), rrr+i*1/12]) for (i, rrr) in enumerate(rr)]
x = np.array(x).transpose((0, 2, 1))
# fig, ax = mpl2.new_fig()
# for i in range(len(rr)):
#     ax.plot(*x[i].T, color="black")


# size_total = (48*axidraw.cm2inch, 48*axidraw.cm2inch)
# size_element=(24*axidraw.cm2inch, 24*axidraw.cm2inch)
size_total = axidraw.dinA_inch[4]
x = axidraw.drawing.scale2(x, size=size_total, padding=axidraw.cm2inch, center=True,
                           keep_aspect=False)
# drawing0 = axidraw.Drawing(x)
# drawing0.render()
# x = axidraw.plotting.get_part(x, i=1, j=1, size_element=size_element, size_total=size_total)
drawing1 = axidraw.Drawing(x)
drawing1.render()
# drawing1 = drawing1.sort_paths()

axidraw.draw(drawing1)


#
# r0 = axidraw.plotting.get_wobbly_line(n=n, m=10, meet_ends="linear-shift", mi=-1, ma=+1, x0=0)
# r1 = axidraw.plotting.get_wobbly_line(n=n, m=10, meet_ends="linear-shift", mi=-1, ma=+1, x0=0)
# r2 = axidraw.plotting.get_wobbly_line(n=n, m=10, meet_ends="linear-shift", mi=-1, ma=+1, x0=0)
# r3 = axidraw.plotting.get_wobbly_line(n=n, m=10, meet_ends="linear-shift", mi=-1, ma=+1, x0=0)
# rr = axidraw.plotting.line_transition(lines=[r0, r1, r2, r3, r0], n=n_years)
#
#
# for i in range(n_years):
#     ax.plot(rr[i]+i*1/n_years, x, color="black")