import datetime

import numpy as np
import axidraw

from wzk import spatial
from wzk import geometry, trajectory, mpl2
from examples.mijorize import util


n = (datetime.date.today() - datetime.date(year=1994, month=7, day=30)).days
# for seed in range(100):
seed = 1
np.random.seed(seed)
dinA = 6

x = np.array([np.random.uniform(low=[0, 0], high=axidraw.dinA_inch[dinA]) for _ in range(n)])

path = []

for i in range(n):
    # theta = np.random.uniform(low=-1.1, high=-0.7)
    theta = np.linalg.norm(x[i])**2 / 5
    v = spatial.transform_2d.theta2dcm(theta)[0]*0.1
    path.append(np.concatenate([x[i:i+1], x[i:i+1]+v]))

paths = axidraw.drawing.scale2(x=path, size=axidraw.dinA_inch[dinA], padding=0.2, keep_aspect=False, center=True,)

paths = axidraw.sort_paths(paths)
drawing = axidraw.Drawing(paths)


ax = drawing.render()

# mpl2.save_fig(file=f"{axidraw.directory}/sup_seed{seed}", fig=ax.figure, formats="jpeg")
# mpl2.close_all()

axidraw.draw(drawing=drawing)
# util.draw_number("090")

