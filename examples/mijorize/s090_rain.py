import numpy as np
import axidraw
from wzk import geometry
from examples.mijorize import util



n = 90
np.random.seed(42)
x = [np.random.uniform(low=[0, 0], high=axidraw.dinA_inch[6]) for _ in range(n)]
r =  np.random.uniform(0.1,0.5, size=n)
path = []

for i in range(n):
    for j in [1, 2, 3, 4, 20]:
        path.append(geometry.get_points_on_circle(x=x[i], r=r[i]/j, n=360, endpoint=True)[0])


x = axidraw.drawing.scale2(x=path, size=axidraw.dinA_inch[6], padding=0.5, keep_aspect=True, center=True,)
drawing = axidraw.Drawing(x)


drawing.render()
axidraw.draw(drawing=drawing)
util.draw_number("090")
