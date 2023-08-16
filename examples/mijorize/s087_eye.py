import numpy as np
import axidraw
from wzk import geometry, perlin
from examples.mijorize import util


n_circle = 1000
n_radius = 1000

np.random.seed(87)
inner_circle = axidraw.plotting.wobbly_circle(n=n_circle, mi=0.3, ma=0.31)
outer_circle = axidraw.plotting.wobbly_circle(n=n_circle, mi=1, ma=1.05)

r0 = perlin.perlin_noise_1d(n=n_radius, m=8, scale=1)
r1 = perlin.perlin_noise_1d(n=n_radius, m=8, scale=1)
r2 = perlin.perlin_noise_1d(n=n_radius, m=8, scale=1)

ra = axidraw.plotting.line_transition(r0, r1, n=333)
rb = axidraw.plotting.line_transition(r1, r2, n=333)
rc = axidraw.plotting.line_transition(r2, r0, n=333)
rr = ra + rb[1:] + rc[1:-1]

paths1 = axidraw.plotting.radial_transition(c0=inner_circle, c1=outer_circle, r=rr, n=100)


inner_circle = axidraw.plotting.wobbly_circle(n=n_circle, mi=0.01, ma=0.02)
outer_circle = axidraw.plotting.wobbly_circle(n=n_circle, mi=0.31, ma=0.31)

r0 = perlin.perlin_noise_1d(n=n_radius, m=8, scale=1)
r1 = perlin.perlin_noise_1d(n=n_radius, m=8, scale=1)
r2 = perlin.perlin_noise_1d(n=n_radius, m=8, scale=1)

ra = axidraw.plotting.line_transition(r0, r1, n=333)
rb = axidraw.plotting.line_transition(r1, r2, n=333)
rc = axidraw.plotting.line_transition(r2, r0, n=333)
rr = ra + rb[1:] + rc[1:-1]
# fig, ax = mpl2.new_fig()
# for i in range(0, n_circle, 20):
#     ax.plot(rr[i]+i*0.1)

paths2 = axidraw.plotting.radial_transition(c0=inner_circle, c1=outer_circle, r=rr, n=100)



x = axidraw.drawing.scale2(x=paths, size=axidraw.dinA_inch[6], padding=0.5, keep_aspect=True, center=True)
drawing = axidraw.Drawing(x[200:])

# drawing.render()
# axidraw.draw(drawing=drawing)
util.draw_number("087")
