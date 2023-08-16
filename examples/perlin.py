import axidraw
import numpy as np
from wzk import np2, mpl2, geometry, grid, perlin_noise_2d, normalize_01


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
# size = np.array(axidraw.A3_SIZE)

size_dinA6 = axidraw.dinA_inch[6]
size_dinA5 = axidraw.dinA_inch[5]

size_total = 5 * np.array(axidraw.dinA_inch[6]) - 4 * axidraw.cm2inch



def create_vector_field(shape, res, seed=None):
    np.random.seed(seed)
    noise = perlin_noise_2d(shape=shape, res=res)
    noise = normalize_01(noise) * 2*np.pi

    vf = np.empty(noise.shape + (2,))
    vf[..., 0] = np.cos(noise)
    vf[..., 1] = np.sin(noise)
    return vf


def simulate_particles(n_particles, n_steps, vf, limits, seed=None):
    np.random.seed(seed)

    x0 = np.random.uniform(low=0, high=1, size=(n_particles, 2))

    x = np.empty((n_particles, n_steps+1, 2))
    x[:, 0, :] = x0.copy()
    for j in range(n_steps):
        i = grid.grid_x2i(x=x[:, j], limits=limits, shape=vf.shape[:2])
        dx = vf[i[:, 0], i[:, 1]] * 0.001
        x[:, j+1] = x[:, j] + dx
        x[:, j+1] = np.clip(x[:, j+1], a_min=0.01, a_max=0.99)

    return x


def prune_boundaries(x):
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
    return paths


def sort_paths_long2short(paths):
    path_lengths = np.array([len(p) for p in paths])
    i_sort = np.argsort(path_lengths)[::-1]
    paths = [paths[i] for i in i_sort]
    return paths


def clean_paths(paths, threshold=0.006):
    paths = sort_paths_long2short(paths)
    grid2 = [[] for _ in paths]

    for i0, p0 in enumerate(paths):
        p0 = np.array(p0)

        path_lengths = np.array([len(p) for p in paths])
        if len(p0) == 0:
            continue

        print(i0, len(p0), path_lengths.sum())
        for i1, p1 in enumerate(paths[i0+1:], start=i0+1):
            p1 = np.array(p1)

            if len(p1) == 0:
                continue

            if grid2[i0] and not set(grid2[i0]).intersection(set(grid2[i1])):
                continue

            d = np.linalg.norm(p0[:, np.newaxis] - p1[np.newaxis, :], axis=-1)
            try:
                j = np.array(np.nonzero(d < threshold)).T
                j = j.min(axis=0)
                paths[i1] = p1[:j[1]]
                grid2[i1].append(i0)
            except ValueError:
                pass
    return paths


def clean_paths2(paths, threshold=0.001):
    paths = sort_paths_long2short(paths)
    limits = np.array([[0.0, 1.0],
                       [0.0, 1.0]])
    shape = np.round(np.ones(2) / threshold).astype(int)

    g = np.zeros(shape, dtype=bool)
    for i, p in enumerate(paths):
        ix = grid.grid_x2i(x=p, limits=limits, shape=shape)
        ib = g[ix[:, 0], ix[:, 1]]

        if any(ib):
            j = np.nonzero(ib)[0][0]
        else:
            j = len(p)

        paths[i] = p[:j]
        g[ix[:j, 0], ix[:j, 1]] = True

    return paths


def remove_short_paths(paths, n0=0):
    paths = [p for p in paths if len(p) > n0]
    return paths


# sort paths by length, this is not smart at all, pretty sure that's even worse than a random permutation
# path_lengths = np.array([len(p) for p in paths])
# i_sort = np.argsort(path_lengths)[::-1]
# paths = [paths[i] for i in i_sort if path_lengths[i] > 10]
#
# print(len(paths))



        # if d.min() < threshold:
        #     print(j)
        #     fig, ax = new_fig(aspect=1)
        #     img = d < threshold
        #     imshow(ax=ax, img=img, mask=~img, cmap='blue')


def get_shortest_path(path):
    se = np.array([p[[0, -1], :] for p in paths2])

    dm_s = np.linalg.norm(se[:, np.newaxis, :1, :] - se[np.newaxis, :, :, :], axis=-1)
    dm_e = np.linalg.norm(se[:, np.newaxis, 1:, :] - se[np.newaxis, :, :, :], axis=-1)

    n = len(dm_s)
    dm_s[range(n), range(n), :] = np.inf
    dm_e[range(n), range(n), :] = np.inf
    l = [0]

    # TODO try random sampling
    #     not the worst time for using genetic algorithms
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

# for i in range(n):
#     dm_s[l[-1]]
#     l[-1]


def get_lengths(paths):
    length_travel = np.array([np.array(p0[0]) - np.array(p1[-1]) for p1, p0 in zip(paths[:-1], paths[1:])])
    length_travel = np.linalg.norm(length_travel, axis=-1).sum()

    length_path = np.array([np.linalg.norm(np.diff(p, axis=0), axis=-1).sum() for p in paths])
    length_path = length_path.sum()

    print(length_travel, length_path)

# drawing = axidraw.Drawing(paths2)
# drawing.render()
# axidraw.draw(drawing=drawing)

#


def plot_occupancy(paths, limits, noise):
    gg = np.zeros((1000, 1000), dtype=bool)
    for i, p in enumerate(paths):
        ix = grid.grid_x2i(p, limits=limits, shape=gg.shape)
        b = gg[ix[:, 0], ix[:, 1]]
        try:
            j = np.nonzero(b)[0][0]
            paths[i] = p[:j]
        except IndexError:
            j = len(p)
        gg[ix[:j, 0], ix[:j, 1]] = True

    fig, ax = mpl2.new_fig(aspect=1)
    mpl2.imshow(ax=ax, img=np.logical_and(-2 < noise, noise < 2))
    mpl2.imshow(ax=ax, img=gg, mask=~gg)


def main():
    dinA = 1
    size = axidraw.dinA_inch[dinA]

    limits = np.array([[0.0, 1.0],
                       [0.0, 1.0]])

    n_steps = 10000
    n_particles = 10000

    vf = create_vector_field(shape=(4096, 4096), res=(8, 8), seed=20221230)
    x = simulate_particles(n_particles=n_particles, n_steps=n_steps, vf=vf, limits=limits)
    for i in range(10):
        x2 = simulate_particles(n_particles=n_particles, n_steps=n_steps, vf=vf, limits=limits)
        x = np.concatenate((x, x2), axis=0)

    x = prune_boundaries(x)
    # x = clean_paths(x, threshold=0.001)
    x = clean_paths2(x, threshold=0.0005)
    x = remove_short_paths(x, n0=10)
    np.save('/Users/jote/Documents/Code/Python/axidraw/data/paths.npy', np.array(x, dtype=object))
    plot(x, size)

    # input("should this be drawn?")
    # drawing = axidraw.Drawing(paths)
    # axidraw.draw(drawing=drawing)



if __name__ == '__main__':
    # main()

    # x = np.load('/Users/jote/Documents/Code/Python/axidraw/data/paths.npy', allow_pickle=True)
    #
    # x = axidraw.drawing.scale2(x, size=size_total, padding=axidraw.cm2inch, mi=0.01, ma=0.99, center=False, keep_aspect=False)
    # x = get_part(x, i=4, j=3)  # vice versa
    #
    # fig, ax = axidraw.drawing.new_fig(axidraw.dinA_inch[6])
    # axidraw.drawing.plot_paths(ax=ax, paths=x, color='k', lw=0.1)

    x = [geometry.box(axidraw.limits_dinA[5])]

    drawing = axidraw.Drawing(x)
    drawing = drawing.sort_paths()

    axidraw.draw(drawing=drawing)


