import numpy as np
import axidraw
from wzk import geometry, trajectory, mpl2
from examples.mijorize import util


n = 200
# for seed in range(100):
seed = 1
dinA = 6
np.random.seed(seed)


n = 450
n_radius = 1000

w_magnitude = 0.05
w0 = axidraw.plotting.get_wobbly_line(n=n, m=20, meet_ends="linear-shift", mi=-w_magnitude, ma=+w_magnitude, x0=0) * 0
w1 = axidraw.plotting.get_wobbly_line(n=n, m=20, meet_ends="linear-shift", mi=-w_magnitude, ma=+w_magnitude, x0=0)
rr = axidraw.plotting.line_transition(lines=[w0, w1, w0], n=29*12, include_end=True)
print(len(rr))
y01 = np.linspace(start=0, stop=1, num=len(rr))
x01_n = np.linspace(start=0, stop=1, num=n)
x = [np.array([x01_n, rrr+yy]) for (rrr, yy) in zip(rr, y01)]

x = np.array(x).transpose((0, 2, 1))

# path = []
# for i, xx in enumerate(x):
#     j0 = 2+i*1
#     j1 = 102+i*1
#
#     path.append(xx[:j0])
#     path.append(trajectory.get_steps_between(xx[j0+10], xx[j1-10], n=10))
#     path.append(xx[j1:])
#     # path.append(xx[j1:])
#     # path.append(np.vstack([x01_n[j0+10:j1-10], np.ones([j1-j0-20])*y01[i]]).T)
#     print(j1)

path = x
x = axidraw.drawing.scale2(x=path, size=axidraw.dinA_inch[dinA], padding=0.5, keep_aspect=False, center=True,)
x = axidraw.sort_paths(x)
drawing = axidraw.Drawing(x)




ax = drawing.render()

# mpl2.save_fig(file=f"{axidraw.directory}/sup_seed{seed}", fig=ax.figure, formats="jpeg")
# mpl2.close_all()

# axidraw.draw(drawing=drawing)
# util.draw_number("090")
