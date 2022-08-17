import matplotlib.pyplot as plt
import numpy as np
from wzk.mpl import new_fig, turn_ticklabels_off, turn_ticks_off, plot_img_patch_w_outlines


import axidraw


def to_bool(s, mode=None):
    if mode is None:
        try:
            int(s)
            mode = 'odds'
        except ValueError:
            mode = 'vowels'

    if mode == 'odds':
        b = __odds2bools(s)

    elif mode == 'vowels':
        b = __vowels2bools(s)
    else:
        raise ValueError

    return b


def __vowels2bools(s):
    vowels = 'aeiouäöü'
    return np.array([ss.lower() in vowels for ss in s])


def __odds2bools(s):
    return np.array([(int(ss) % 2) == 1 for ss in s])


def get_initial_rows(a, b, mode='vowels'):
    return to_bool(a), to_bool(b)


def make_grid(a, b):
    a = np.hstack([[False], a])
    ia, ib = np.meshgrid(range(len(b)), range(len(a)), indexing='ij')
    aaa = (ia + a[np.newaxis, :]) % 2 == 1
    bbb = (ib + b[:, np.newaxis]) % 2 == 1

    grid = np.concatenate([aaa[:1, :], bbb], axis=0)
    grid[0] = (np.cumsum(grid[0]) % 2) == 1
    grid = (np.cumsum(grid, axis=0) % 2) == 1
    grid = grid.T
    grid = grid[:, ::-1]

    return grid


def plot_grid(grid):

    fig, ax = new_fig(aspect=1)
    limits = np.array([[0, grid.shape[0]],
                       [0, grid.shape[1]]])

    limits2 = np.array([[0, grid.shape[1]],
                        [0, grid.shape[0]]])

    # imshow(ax=ax, img=grid, limits=limits2, cmap='blue', mask=~grid, alpha=0.5)
    plot_img_patch_w_outlines(ax=ax, img=grid, limits=limits, alpha_patch=0.5, hatch='//////', lw=0.5)
    ax.set_xlim(-1, limits[0, 1]+1)
    ax.set_ylim(-1, limits[1, 1]+1)
    # turn_ticklabels_off(ax=ax, axes='xy')
    # turn_ticks_off(ax=ax)


def plot_stitches(ia, ib):
    grid = make_grid(a=ia, b=ib)

    na = len(ia)
    nb = len(ib)

    x = np.zeros((na, nb, 2, 2))
    x[:, :, 0, 0] = np.arange(na)[:, np.newaxis]
    x[:, :, 1, 0] = np.arange(na)[:, np.newaxis] + 1
    x[:, :, :, 1] = np.arange(nb)[np.newaxis, :, np.newaxis]
    x = x[::2, :, :, :]
    x[:, ib, :, 0] += 1

    y = np.zeros((nb, na, 2, 2))
    y[:, :, 0, 1] = np.arange(nb)[:, np.newaxis]
    y[:, :, 1, 1] = np.arange(nb)[:, np.newaxis] + 1
    y[:, :, :, 0] = np.arange(1, na+1)[np.newaxis, :, np.newaxis]
    y = y[::2, :, :, :]
    y[:, ia, :, 1] += 1

    fig, ax = new_fig(aspect=1)

    def __plot(xx, color):
        for i in range(xx.shape[0]):
            for j in range(xx.shape[1]):
                ax.plot(xx[i, j, :, 0], xx[i, j, :, 1], color=color, ls='-', lw=3)

    __plot(x, color='red')
    __plot(y, color='blue')

    return x, y


def main(a, b):
    a = a.strip()
    b = b.strip()
    ia, ib = get_initial_rows(a=a, b=b)
    grid = make_grid(a=ia, b=ib)

    # plot_grid(~grid)
    # plot_grid(~grid)
    x, y = plot_stitches(ia=ia, ib=ib)

    limits = np.array([[-0.1, grid.shape[0]],
                       [-0.1, grid.shape[1]]])

    x_path = stitches2path(x=x, limits=limits)
    y_path = stitches2path(x=y, limits=limits)
    print(limits)
    print(x_path.shape)
    mi = np.array((0., 0.))
    ma = np.array((len(ia), len(ib)))
    print(ma)
    x_path = axidraw.drawing.scale2(x=x_path, size=axidraw.dinA_inch[6], mi=mi, ma=ma, padding=0.5, keep_aspect=True)
    y_path = axidraw.drawing.scale2(x=y_path, size=axidraw.dinA_inch[6], mi=mi, ma=ma, padding=0.5, keep_aspect=True)
    y_path[:, :, 0] -= (x_path[0, 1, 0] - x_path[0, 0, 0])
    x_path[:, :, 1] += 0.8
    y_path[:, :, 1] += 0.8
    # drawing = axidraw.Drawing(x_path.tolist())  # red
    drawing = axidraw.Drawing(y_path.tolist())  # blue
    axidraw.draw(drawing=drawing)


    fig, ax = new_fig(aspect=1, width=axidraw.dinA_inch[6][0], height=axidraw.dinA_inch[6][1])
    ax.set_xlim(0, axidraw.dinA_inch[6][0])  # TODO turn limits to make it consistent with everything
    ax.set_ylim(0, axidraw.dinA_inch[6][1])
    # TODO turn limits to make it consistent with everything

    for xx in x_path:
        ax.plot(xx[:, 0], xx[:, 1], color='red', ls='-', lw=3)
        plt.pause(0.01)

    for yy in y_path:
        ax.plot(yy[:, 0], yy[:, 1], color='blue', ls='-', lw=3)
        plt.pause(0.01)


def stitches2path(x, limits):
    path = []
    for i in range(x.shape[1]):
        xx = x[:, i]
        if np.any(xx[-1, 1] >= limits[:, 1]):
            xx = xx[:-1]
        if i % 2 == 1:
            xx = xx[::-1, :, :]
            xx = xx[:, ::-1, :]
        path += xx.tolist()

    return np.array(path)


if __name__ == '__main__':
    # main(a='LisaSophiaTenhumberg', b='JohannesValentinHamm')
    # main(a='Julia', b='Hamm')
    # main(a='Johannes', b='Tenhumberg')
    # main(a='Theresa', b='Tenhumberg')

    main(b='FabianWaldenmaier',
         a='CharlotteKonkel'[::-1])

    # main(b='Ein Teil des Teils der Anfangs alles war',
    #      a='Ein Teil der Finsternis, die sich das Licht gebar')
