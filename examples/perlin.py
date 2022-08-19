import axidraw
import numpy as np
from wzk import grid_x2i, perlin_noise_2d, normalize_01
from wzk.mpl import new_fig, plt, imshow


# size = np.array(axidraw.A3_SIZE)

limits = np.array([[0.0, 1.0],
                   [0.0, 1.0]])
n_steps = 2000
n_particles = 10000

x0 = np.random.uniform(low=0, high=1, size=(n_particles, 2))
# x0 = np.array(np.meshgrid(*[np.linspace(0.05, 0.95, 100)]*2))
# x0 = x0.reshape((2, -1)).T
# x0 += np.random.normal(loc=0, scale=0.05, size=x0.shape)
# x0 = np.clip(x0, a_min=0.01, a_max=0.99)

noise = perlin_noise_2d(shape=(1024, 1024), res=np.array((16, 8)))
noise = normalize_01(noise) * 2*np.pi
# noise = 2*np.pi*np.random.random((1000, 1000))
# noise = 2*np.pi*np.random.normal(loc=0, scale=0.1, size=(1000, 1000))

v = np.empty(noise.shape + (2,))
v[..., 0] = np.cos(noise)
v[..., 1] = np.sin(noise)


x = np.empty((n_particles, n_steps+1, 2))
x[:, 0, :] = x0.copy()

for j in range(n_steps):
    i = grid_x2i(x=x[:, j], limits=limits, shape=noise.shape)
    x[:, j+1] = x[:, j] + v[i[:, 0], i[:, 1]] * 0.001
    x[:, j+1] = np.clip(x[:, j+1], a_min=0.01, a_max=0.99)



# fig, ax = new_fig(aspect=1)
# ax.set_xlim(0, 1)
# ax.set_ylim(0, 1)
count = 0
paths = []
for xx in x:
    if any(xx[0, :] <= 0.01) or any(xx[0, :] >= 0.99):
        count += 1
        continue
    try:
        i = np.nonzero(xx == 0.01)[0][0]
        xx = xx[:i]
    except IndexError:
        pass

    try:
        i = np.nonzero(xx == 0.99)[0][0]
        xx = xx[:i]
    except IndexError:
        pass

    paths.append([(xxx[0], xxx[1]) for xxx in xx])
    # ax.plot(*xx.T, color='black', lw=0.1)


gg = np.zeros((1000, 1000), dtype=bool)
for i, p in enumerate(paths):
    ix = grid_x2i(p, limits=limits, shape=gg.shape)
    b = gg[ix[:, 0], ix[:, 1]]
    try:
        j = np.nonzero(b)[0][0]
        paths[i] = p[:j]
    except IndexError:
        j = len(p)
    gg[ix[:j, 0], ix[:j, 1]] = True


# threshold = 0.006
#
# path_lengths = np.array([len(p) for p in paths])
# i_sort = np.argsort(path_lengths)[::-1]
# paths = [paths[i] for i in i_sort]
#
#
# grid2 = [[] for p in paths]
#
# for i0, p0 in enumerate(paths):
#     p0 = np.array(p0)
#
#     path_lengths = np.array([len(p) for p in paths])
#     if len(p0) == 0:
#         continue
#
#     print(i0, len(p0), path_lengths.sum())
#     for i1, p1 in enumerate(paths[i0+1:], start=i0+1):
#         if len(p1) == 0:
#             continue
#
#         if grid2[i0] and not set(grid2[i0]).intersection(set(grid2[i1])):
#             continue
#
#         p1 = np.array(p1)
#         d = np.linalg.norm(p0[:, np.newaxis] - p1[np.newaxis, :], axis=-1)
#         try:
#             j = np.array(np.nonzero(d < threshold)).T
#             j = j.min(axis=0)
#             paths[i1] = p1[:j[1]]
#             grid2[i1].append(i0)
#         except ValueError:
#             pass


path_lengths = np.array([len(p) for p in paths])
i_sort = np.argsort(path_lengths)[::-1]
paths = [paths[i] for i in i_sort if path_lengths[i] > 10]

print(len(paths))


fig, ax = new_fig(aspect=1)
ax.set_xlim(0, axidraw.dinA_inch[6][0])
ax.set_ylim(0, axidraw.dinA_inch[6][1])


paths2 = []
for p in paths:
    p = np.array(p)
    p = axidraw.drawing.scale2(p, size=axidraw.dinA_inch[6], padding=0.5, mi=0.01, ma=0.99, keep_aspect=False, center=False)
    paths2.append(p)
    # paths.append([(xxx[0], xxx[1]) for xxx in xx])

    ax.plot(*p.T, color='black', lw=0.1)

    # if d.min() < threshold:
    #     print(j)
    #     fig, ax = new_fig(aspect=1)
    #     img = d < threshold
    #     imshow(ax=ax, img=img, mask=~img, cmap='blue')


se = np.array([p[[0, -1], :] for p in paths2])

dm_s = np.linalg.norm(se[:, np.newaxis, :1, :] - se[np.newaxis, :, :, :], axis=-1)
dm_e = np.linalg.norm(se[:, np.newaxis, 1:, :] - se[np.newaxis, :, :, :], axis=-1)

n = len(dm_s)
dm_s[range(n), range(n), :] = np.inf
dm_e[range(n), range(n), :] = np.inf
l = [0]

for i in range(n):

    dm_s[l[-1]]
    l[-1]




def get_lengths(paths):
    length_travel = np.array([np.array(p0[0]) - np.array(p1[-1]) for p1, p0 in zip(paths[:-1], paths[1:])])
    length_travel = np.linalg.norm(length_travel, axis=-1).sum()

    length_path = np.array([np.linalg.norm(np.diff(p, axis=0), axis=-1).sum() for p in paths])
    length_path = length_path.sum()

    print(length_travel, length_path)
# drawing = axidraw.Drawing(paths2)
# axidraw.draw(drawing=drawing)
# TODO
#    1. make good TSP planner
#      this can complete in the background, as the first lines are already drawn, the same for pruning ang cleaning of
#      the paths,
#    2. make tree structure for poisson disk
#       make it more efficient by using the grid properly
#       make the path drawing more efficient, draw every path exactly twice,
#       compare with previous paths lengths
#
#    2. look under the hood and understand how the paths are made smooth and fast, is there room for improvement?
#    3.
#
# for _ in range(10000):
#     i = np.random.permutation(np.arange(len(paths)))
#     j0 = np.random.randint(low=0, high=2, size=len(paths))
#     j1 = 1 - j0
# 
#     xx0 = x01[j0, np.arange(len(paths))][i]
#     xx1 = x01[j1, np.arange(len(paths))][i]
#     d = np.linalg.norm(np.diff(xx1[:-1] - xx0[1:]), axis=-1).sum()
# 
#     if d < d_min:
#         d_min = d
#         print(d)


# imshow(ax=ax, img=np.logical_and(-2 < noise, noise < 2))
# fig, ax = new_fig(aspect=1)
# imshow(ax=ax, img=gg, mask=~gg)

# input("should this be drawn?")
# drawing = axidraw.Drawing(paths)
# axidraw.draw(drawing=drawing)
