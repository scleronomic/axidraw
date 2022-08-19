import numpy as np
from wzk.numpy2 import grid_x2i
from wzk.mpl import new_fig, plt, imshow, grid_lines


def ccw(a, b, c):
    return (b[..., 0] - a[..., 0]) * (c[..., 1] - a[..., 1]) > (b[..., 1] - a[..., 1]) * (c[..., 0] - a[..., 0])


# Return true if line segments AB and CD intersect
def intersect(a, b, c, d):
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)


d = 2
k = 100
r = 0.05
n = int(np.ceil(np.sqrt(d)/r))


grid = np.full((n,)*d, -1)
limits = np.array([[-1.0, +1.0],
                   [-1.0, +1.0]])

# for xx in x:
#     ax.plot(*xx, color='black', marker='o', markersize=1)


class Branch:
    def __init__(self, parent):
        self.parent = parent
        self.leaves = []


class Tree:
    def __init__(self, root, n=10000):
        self.length = 1
        self.points = np.zeros((n, 2), dtype=float)
        self.points[0] = root
        self.parents = np.zeros(n, dtype=int)
        self.parents[0] = -1
        self.children = np.zeros(n, dtype=object)
        self.children[0] = []
        self.depths = np.zeros(n, dtype=int)
        self.depths_max = np.zeros(n, dtype=int)

    def add(self, point, parent):
        i = self.length
        self.points[i] = point
        self.parents[i] = parent
        self.children[i] = np.array([], dtype=int)
        self.children[parent] = np.hstack([self.children[parent], [i]]).astype(int)
        self.depths[i] = self.depths[parent] + 1
        self.length += 1

    def prune(self):
        self.points = self.points[:self.length]
        self.parents = self.parents[:self.length]
        self.children = self.children[:self.length]
        self.depths = self.depths[:self.length]

    def get_depths_max(self):
        leaves = np.array([len(c) == 0 for c in self.children], dtype=bool)
        self.depths_max = self.depths

        for l in np.nonzero(leaves)[0]:
            i = l
            while i != 0:
                p = self.parents[i]
                self.depths_max[p] = max(self.depths_max[p], self.depths_max[i])
                i = p

    def make_path(self):
        path = [0]
        visited = np.zeros(self.length, dtype=bool)
        visited[0] = True
        while not all(visited):
            i = path[-1]
            c = self.children[i]
            dc = self.depths_max[c]
            vc = visited[c]

            dc = dc[~vc]
            c = c[~vc]

            if len(dc) == 0:
                path.append(self.parents[i])

            else:
                c = c[np.argmax(dc)]
                path.append(c)
                visited[c] = True

        return np.array(path)


def aaa(t):
    # fig, ax = new_fig(aspect=1)
    # ax.set_axis_off()
    # ax.set_xlim(-1, +1)
    # ax.set_ylim(-1, +1)
    # grid_lines(ax=ax, start=limits[:, 0], step=r/np.sqrt(d), limits=limits)

    x0 = np.zeros(d)
    x = x0[np.newaxis, :].copy()
    # x[:, 1] = -1
    # x = np.array([[-0.8, -0.0],
    #               [-0.6, -0.0],
    #               [-0.4, -0.0],
    #               [-0.2, -0.0],
    #               [+0.0, -0.0],
    #               [+0.2, -0.0],
    #               [+0.4, -0.0],
    #               [+0.6, -0.0],
    #               [+0.8, -0.0],
    #               ])
    i = grid_x2i(x, limits=limits, shape=grid.shape)
    grid[i[:, 0], i[:, 1]] = np.arange(len(x))
    h = None
    active = [True] * len(x)
    count = 0
    tree = Tree(root=x0, n=21000)
    while np.any(active):
        i = np.random.randint(0, np.sum(active))
        i = np.nonzero(active)[0][i]

        active[i] = False
        # print(np.size(active), np.sum(active), count)
        for _ in range(k):
            _r = np.random.uniform(low=r, high=2*r, size=d)
            if i == 0:
                # phi = np.random.uniform(low=np.pi/3+0.8, high=2/3*np.pi-0.8)
                phi = np.random.normal(loc=np.pi/2, scale=t)
            else:
                dd = x[i] - x0
                # phi = np.random.normal(loc=np.arctan2(dd[1], dd[0]), scale=t)
                phi = np.random.normal(loc=np.pi/2, scale=t)

            x1 = x[i] + np.array([np.cos(phi), np.sin(phi)]) * _r
            # if x1[1] > 1:
            if np.linalg.norm(x1-x0) > 1:
                continue

            i1 = grid_x2i(x1, limits=limits, shape=grid.shape)
            if any(i1 < 0) or any(i1 >= np.array(grid.shape)):
                continue

            # if all(np.linalg.norm(x1 - x, axis=-1) >= r):
            if grid[i1[0], i1[1]] == -1:
                grid[i1[0], i1[1]] = len(x) + 1
                x = np.concatenate([x, x1[np.newaxis, :]])
                tree.add(point=x1, parent=i)
                active += [True]
                active[i] = True
                count += 1

                # ax.plot(*x1, color='black', marker='o', markersize=1)
                # ax.plot((x[i, 0], x1[0]), (x[i, 1], x1[1]), color='black', lw=0.5)
                # h = imshow(ax=ax, h=h, img=grid, limits=limits, cmap='black', alpha=0.1, mask=grid != -1)
                if count % 100 == 0:
                    pass
                    # plt.pause(0.001)

            if count == 20000:
                break

        if count == 20000:
            break

    return tree


# np.random.seed(51)
tree = aaa(2*np.pi)
tree.prune()
tree.get_depths_max()
path_i = tree.make_path()
path = tree.points[path_i]



import axidraw

path = axidraw.drawing.scale2(x=path, size=axidraw.dinA_inch[6], padding=0.5, keep_aspect=True)

fig, ax = new_fig(aspect=1)
ax.set_xlim(0, axidraw.dinA_inch[6][0])
ax.set_ylim(0, axidraw.dinA_inch[6][1])
ax.plot(*path.T, color='black', lw=0.5)
#
#
# i = np.random.permutation(np.arange(100, tree.length))[:28]
# points = axidraw.drawing.scale2(x=tree.points, size=axidraw.dinA_inch[6], padding=1, keep_aspect=False)
# pi = points[i]
# ax.plot(*pi.T, color='black', ls='', marker='o', markersize=3)
#

# drawing = axidraw.Drawing([path])
# axidraw.draw(drawing=drawing)
#
# path[:, 1] += 1
# fig, ax = new_fig(aspect=1)
# ax.set_xlim(0, axidraw.dinA_inch[6][0])
# ax.set_ylim(0, axidraw.dinA_inch[6][1])
# ax.plot(*path.T, color='black', lw=0.5)
# for i in range(len(path)-1):
#     ax.plot(*path[i:i+2, :].T, color='black', lw=0.5)
#     plt.pause(0.01)

# for tt in [np.pi/15, np.pi/20, np.pi/25]:
#     aaa(tt)
#
#
# for i in range(5):
#     aaa(np.pi/25)