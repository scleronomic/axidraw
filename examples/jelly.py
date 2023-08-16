from wzk import mp2, random2


import numpy as np
import axidraw
from wzk import geometry, perlin
from examples.mijorize import util


n_circle = 1000
n_radius = 1000

np.random.seed(87)
inner_circle = axidraw.plotting.wobbly_circle(n=n_circle, mi=0.3, ma=0.35)
outer_circle = axidraw.plotting.wobbly_circle(n=n_circle, mi=1, ma=1.05)

r0 = perlin.perlin_noise_1d(n=n_radius, m=8, scale=1)
r1 = perlin.perlin_noise_1d(n=n_radius, m=8, scale=1)
r2 = perlin.perlin_noise_1d(n=n_radius, m=8, scale=1)

ra = axidraw.plotting.line_transition(r0, r1, n=333)
rb = axidraw.plotting.line_transition(r1, r2, n=333)
rc = axidraw.plotting.line_transition(r2, r0, n=333)

