import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

points = np.random.random((50, 2))
vor = Voronoi(points)

fig = voronoi_plot_2d(vor)
plt.show()
