import numpy as np

from wzk import mpl2, ltd

from axidraw.paths import (simplify_paths, sort_paths, join_paths, crop_paths,
                           convex_hull, expand_quadratics, paths_length)


class Drawing(object):
    def __init__(self, paths=None):
        self.paths = paths or []
        self._bounds = None
        self._length = None
        self._down_length = None
        self._hull = None

    def dirty(self):
        self._bounds = None
        self._length = None
        self._down_length = None
        self._hull = None

    @classmethod
    def loads(cls, data):
        paths = []
        for line in data.split('\n'):
            line = line.strip()
            if line.startswith('#'):
                continue
            path = line.split()
            path = [tuple(map(float, x.split(','))) for x in path]
            path = expand_quadratics(path)
            if path:
                paths.append(path)
        return cls(paths)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as fp:
            return cls.loads(fp.read())

    def dump_str(self):
        lines = []
        for path in self.paths:
            lines.append(' '.join('%f,%f' % (x, y) for x, y in path))
        return '\n'.join(lines)

    def dump(self, filename):
        with open(filename, 'w') as fp:
            fp.write(self.dump_str())

    def dumps_svg(self, scale=96):
        lines = []
        w = (self.width + 2) * scale
        h = (self.height + 2) * scale
        lines.append('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="%g" height="%g">' % (w, h))
        lines.append('<g transform="scale(%g) translate(1 1)">' % scale)
        for path in self.paths:
            p = []
            c = 'M'
            for x, y in path:
                p.append('%s%g %g' % (c, x, y))
                c = 'L'
            d = ' '.join(p)
            lines.append('<path d="%s" fill="none" stroke="black" stroke-width="0.01" stroke-linecap="round" stroke-linejoin="round" />' % d)
        lines.append('</g>')
        lines.append('</svg>')
        return '\n'.join(lines)

    def dump_svg(self, filename):
        with open(filename, 'w') as fp:
            fp.write(self.dumps_svg())

    @property
    def points(self):
        return [(x, y) for path in self.paths for x, y in path]

    @property
    def convex_hull(self):
        if self._hull is None:
            self._hull = convex_hull(self.points)
        return self._hull

    @property
    def bounds(self):
        if self._bounds is None:
            points = self.points
            if points:
                x1 = min(x for x, y in points)
                x2 = max(x for x, y in points)
                y1 = min(y for x, y in points)
                y2 = max(y for x, y in points)
            else:
                x1 = x2 = y1 = y2 = 0
            self._bounds = (x1, y1, x2, y2)
        return self._bounds

    @property
    def length(self):
        if self._length is None:
            length = self.down_length
            for p0, p1 in zip(self.paths, self.paths[1:]):
                x0, y0 = p0[-1]
                x1, y1 = p1[0]
                length += np.hypot(x1 - x0, y1 - y0)
            self._length = length
        return self._length

    @property
    def up_length(self):
        return self.length - self.down_length

    @property
    def down_length(self):
        if self._down_length is None:
            self._down_length = paths_length(self.paths)
        return self._down_length

    @property
    def width(self):
        x1, y1, x2, y2 = self.bounds
        return x2 - x1

    @property
    def height(self):
        x1, y1, x2, y2 = self.bounds
        return y2 - y1

    @property
    def size(self):
        return self.width, self.height

    @property
    def all_paths(self):
        result = []
        position = (0, 0)
        for path in self.paths:
            result.append([position, path[0]])
            result.append(path)
            position = path[-1]
        result.append([position, (0, 0)])
        return result

    def simplify_paths(self, tolerance):
        return Drawing(simplify_paths(self.paths, tolerance))

    def sort_paths(self, reversible=True):
        return Drawing(sort_paths(self.paths, reversible))

    def join_paths(self, tolerance):
        return Drawing(join_paths(self.paths, tolerance))

    def crop_paths(self, x1, y1, x2, y2):
        return Drawing(crop_paths(self.paths, x1, y1, x2, y2))

    def remove_duplicates(self):
        pass
        # TODO

    def add(self, drawing):
        self.paths.extend(drawing.paths)
        self.dirty()

    def transform(self, func):
        return Drawing([[func(x, y) for x, y in path] for path in self.paths])

    def translate(self, dx, dy):
        def func(x, y):
            return x + dx, y + dy
        return self.transform(func)

    def scale(self, sx, sy=None):
        if sy is None:
            sy = sx

        def func(x, y):
            return x * sx, y * sy
        return self.transform(func)

    def rotate(self, angle):
        c = np.cos(np.deg2rad(angle))
        s = np.sin(np.deg2rad(angle))

        def func(x, y):
            return x * c - y * s, y * c + x * s
        return self.transform(func)

    def move(self, x, y, ax, ay):
        x1, y1, x2, y2 = self.bounds
        dx = x1 + (x2 - x1) * ax - x
        dy = y1 + (y2 - y1) * ay - y
        return self.translate(-dx, -dy)

    def origin(self):
        return self.move(0, 0, 0, 0)

    def center(self, width, height):
        return self.move(width / 2, height / 2, 0.5, 0.5)

    def rotate_to_fit(self, width, height, step=5):
        for angle in range(0, 180, step):
            drawing = self.rotate(angle)
            if drawing.width <= width and drawing.height <= height:
                return drawing.center(width, height)
        return None

    def scale_to_fit_height(self, height, padding=0):
        return self.scale_to_fit(1e9, height, padding)

    def scale_to_fit_width(self, width, padding=0):
        return self.scale_to_fit(width, 1e9, padding)

    def scale_to_fit(self, width, height, padding=0):
        width -= padding * 2
        height -= padding * 2
        scale = min(width / self.width, height / self.height)
        return self.scale(scale, scale).center(width, height)

    def rotate_and_scale_to_fit(self, width, height, padding=0, step=1):
        values = []
        width -= padding * 2
        height -= padding * 2
        hull = Drawing([self.convex_hull])
        for angle in range(0, 180, step):
            d = hull.rotate(angle)
            scale = min(width / d.width, height / d.height)
            values.append((scale, angle))
        scale, angle = max(values)
        return self.rotate(angle).scale(scale, scale).center(width, height)

    def remove_paths_outside(self, width, height):
        e = 1e-8
        paths = []
        for path in self.paths:
            ok = True
            for x, y in path:
                if x < -e or y < -e or x > width + e or y > height + e:
                    ok = False
                    break
            if ok:
                paths.append(path)
        return Drawing(paths)

    def render(self, line_width=None,
               ax=None):
        if ax is None:
            fig, ax = mpl2.new_fig(aspect=1)

        for xx in self.paths:
            if len(xx) > 1:
                xx = np.array(xx)
                ax.plot(*xx.T, color='black')

        return ax

def paths_wrapper(paths):
    if paths is None:
        return []

    if isinstance(paths, np.ndarray):
        if paths.ndim == 1 or paths.shape[1] == 3:
            paths = [np.array(p) for p in paths]
        elif paths.ndim == 2:
            paths = [np.array(paths)]
        elif paths.ndim == 3:
            paths = [np.array(p) for p in paths]
        else:
            raise ValueError('Invalid paths array')

    elif isinstance(paths, list):
        if ltd.depth(paths) == 2:
            paths = [np.array(paths)]
        elif ltd.depth(paths) == 3:
            paths = [np.array(p) for p in paths]
    else:
        raise ValueError('Invalid paths list')

    return paths


def get_min_max(x):
    x = np.concatenate(x, axis=0).reshape(-1, 2)
    mi = x.min(axis=0)
    ma = x.max(axis=0)
    return mi, ma


def scale2(x, size, padding, mi=None, ma=None, keep_aspect=True, center=True):
    x = paths_wrapper(x)

    size, padding = np.atleast_1d(size, padding)
    scale = np.ones(2) * (size - 2 * padding)

    if mi is None:
        mi = get_min_max(x)[0]

    if ma is None:
        ma = get_min_max(x)[1]

    scale_ = (scale / (ma - mi))

    if keep_aspect:
        scale_ = scale_.min()

    for i in range(len(x)):
        xi = x[i]
        xi -= mi

        xi *= scale_
        xi += padding

        if center:
            d = size - ((ma - mi) * scale_ + 2*padding)
            xi += d/2
        x[i] = xi

    return x


def new_fig(size):
    fig, ax = mpl2.new_fig(aspect=1)
    ax.set_xlim(0, size[0])
    ax.set_ylim(0, size[1])
    return fig, ax


def plot_paths(ax, paths, **kwargs):

    kwargs['lw'] = kwargs.pop('lw', 0.1)
    kwargs['color'] = kwargs.pop('color', 'black')
    for p in paths:
        ax.plot(*p.T, **kwargs)

