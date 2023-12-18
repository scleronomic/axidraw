import numpy as np

import datetime

from astropy.time import Time
from astroquery.jplhorizons import Horizons

from wzk import mpl2, math2, geometry, trajectory


scale_orbit = [1, 1, 1, 1, 0.4, 0.3, 0.2, 0.15]
scale_size = [1, 0.6, 0.6, 1, 0.1, 0.1, 0.2, 0.2]

planet_sizes = dict(mercury=2440,
                    venus=6052,
                    earth=6371,
                    mars=3390,
                    jupiter=69911,
                    saturn=58232,
                    uranus=25362,
                    neptune=24622)
planet_period = dict(mercury=88,
                     venus=225,
                     earth=365,
                     mars=687,
                     jupiter=12*365,
                     saturn=29*365,
                     uranus=84*365,
                     neptune=165*365)
names = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']


def str2date(date):
    return datetime.datetime.fromisoformat(date)


def date2str(date):
    return date.strftime("%Y-%m-%d")


def date2astro(date):
    if not isinstance(date, str):
        date = date2str(date)
    return Time(date).jd


def simulate_orbit(x, v, n):
    dt = 1.0

    x_list = np.zeros((n, 3))

    x_list[0] = x

    for i in range(1, n):
        x_list[i] = x_list[i-1] + v * dt
        acc = -2.959e-4 * x_list[i] / np.sum(x_list[i] ** 2) ** (3. / 2)  # in units of AU/day^2
        v += acc * dt

    return  x_list


def get_orbit(planet, date, return_2d=True):
    if isinstance(date, str):
        date = str2date(date)

    if isinstance(planet, str):
        planet = names.index(planet.lower())

    orbital_period = planet_period[names[planet]]
    dt = int(orbital_period * 0.05)

    obj = Horizons(id=planet+1, location="@sun", epochs=date2astro(date)).vectors()
    x0 = np.array([float(obj[xi]) for xi in ["x", "y", "z"]])
    v0 = np.array([float(obj[vxi]) for vxi in ["vx", "vy", "vz"]])

    x = simulate_orbit(x=x0, v=v0, n=orbital_period+dt)


    # add safety margin to get exactly one full orbit
    theta0 = np.arctan2(x[0, 1], x[0, 0])
    theta1 = np.arctan2(x[-2*dt:, 1], x[-2*dt:, 0])
    dtheta = math2.angle2minuspi_pluspi(theta1-theta0)
    print(names[planet])
    print(dtheta)
    i_end = np.nonzero(dtheta > 0)[0][0]
    i_end = -2*dt+i_end+1
    x = x[:i_end, :]

    if return_2d:
        return x[:, :2]
    else:
        return x
# def main():



def get_all_orbits(date):
    x = []
    for i, planet in enumerate(names):
        x.append(get_orbit(planet=planet, date=date) * scale_orbit[i])

    return x


date = "2021-11-21"

x_all = get_all_orbits(date=date)

r_all = []
fig, ax = mpl2.new_fig(aspect=1)
for i, xx in enumerate(x_all):
    ax.plot(*xx.T, color="black")
    rr = geometry.get_points_on_circle(x=xx[0], r=planet_sizes[names[i]]/30000 * scale_size[i], n=360, endpoint=True)
    r_all.append(rr.squeeze())
    ax.plot(*rr.T, color="red")

ax.plot(*np.array([xx[0] for xx in x_all]).T, color="black")

# for i in range(8):
#     for j in range(365):
#         ji0 = j % len(x_all[i])
#         ji1 = j % len(x_all[i+1])
#         ax.plot([x_all[i][ji0, 0], x_all[i+1][ji1, 0]],
#                 [x_all[i][ji0, 1], x_all[i+1][ji1, 1]],
#                 color="black")


# axidraw
import axidraw
from axidraw import lines


x_all = [trajectory.get_path_adjusted(x=xx, n=1000) for xx in x_all]
mi, ma = axidraw.drawing.get_min_max(x_all)
# x = axidraw.drawing.scale2(x=x_all, size=axidraw.dinA_inch[5], padding=0.5, keep_aspect=True, center=True)
x = axidraw.drawing.scale2(x=r_all, size=axidraw.dinA_inch[5], padding=0.5, keep_aspect=True, center=True, mi=mi, ma=ma)
drawing = axidraw.Drawing(x)

# p = lines.draw_lines(font=None, lines=["2023", "06", "05"], upper_left=(1, 1), lineheight=0.3, point_size=16,
#                      rotate=180)
# drawing = axidraw.Drawing(axidraw.drawing.paths_wrapper(paths=p))


# drawing = axidraw.Drawing([geometry.box(axidraw.limits_dinA[5])])
drawing.render()
# axidraw.draw(drawing=drawing)
