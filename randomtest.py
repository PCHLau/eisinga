from skyfield.api import load
from skyfield.api import utc
import skyfield.framelib as fb
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R
import scipy.optimize
import functools
import datetime
import math
import weakref

ts = load.timescale()
now = ts.now()

# time=[]

period  = 100

today = datetime.datetime(2024, 1, 1, tzinfo=utc)

# for i in range(1,100):
#     time.append(ts.from_datetime(today))
#     today += datetime.timedelta(days=1000)

planets = load('de440.bsp')

objects = [
            {'name': 'sun', 'orbper': 365.256363004}
            ,{'name': 'earth', 'orbper': 365.256363004}
            ,{'name': 'moon', 'orbper': 365.256363004}
            ,{'name': 'mercury', 'orbper': 87.9691}
            ,{'name': 'venus', 'orbper':224.701}
            ,{'name': 'mars', 'orbper': 686.980}
            ,{'name': 'jupiter', 'orbper': 4332.59}
            ,{'name': 'saturn', 'orbper': 10755.70}
            ,{'name': 'uranus', 'orbper': 30688.5}
            ,{'name': 'neptune', 'orbper': 60195}
            ,{'name': 'pluto', 'orbper': 90560}
           ]

new_data = []

fig = plt.figure()
ax = fig.add_subplot()

x_max = 0
y_max = 0
x_min = 0
y_min = 0

time = []

for i in range(1,100):
    time.append(ts.from_datetime(today))
    today += datetime.timedelta(days=period)

x_maxmax = 0
y_maxmax = 0
x_minmin = 0
y_minmin = 0

for i, el in enumerate(objects):
    if el['name'] in ['sun', 'earth', 'moon']:
        obj = planets[el['name']]
    else:
        obj = planets[f'{el['name']} barycenter']

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    color = colors[i%len(colors)]

    loc = []

    orbper = el['orbper']
    orbper = math.ceil(orbper*1.1)

    if i == 0:
        time_copy = time.copy()
    else:
        pass
        

    loops = math.ceil(orbper/period)

    delta = time_copy[-1] - time_copy[0]


    if delta < orbper:
        for timedelta in range(1, int((orbper-delta)//period)):
            time_copy.append(ts.from_datetime(today))
            today += datetime.timedelta(days=period)

        orbit_time = time_copy
    else:
        orbit_time = time_copy[:loops]


    for j, t in enumerate(orbit_time):
        location = obj.at(t).position.km

        rot = fb.ecliptic_frame.rotation_at(t)
        r = R.from_matrix(rot)

        location = r.apply(location)
        loc.append(location)

    x = []
    y = []
    z = []

    for k, a in enumerate(loc):
        x.append(loc[k][0])
        y.append(loc[k][1])
        z.append(loc[k][2])

    el['x'] = x
    el['y'] = y
    el['z'] = z
    el['color'] = color

    X = np.array([[x[0]]])
    Y = np.array([[y[0]]])

    for j,b in enumerate(x):
        if j == 0:
            continue
        X = np.append(X, [[x[j]]], axis=0)
        Y = np.append(Y, [[y[j]]], axis=0)

    A = np.hstack([X**2, X * Y, Y**2, X, Y])
    b = np.ones_like(X)
    xx = np.linalg.lstsq(A, b)[0].squeeze()

    # plt.scatter(x, y, color=color, s=0.5)



    x_min = X.min()+X.min()/10
    x_max = X.max()+X.max()/10
    y_min = Y.min()+Y.min()/10
    y_max = Y.max()+Y.max()/10

    x_maxmax = max(x_max, x_maxmax)
    y_maxmax = max(y_max, y_maxmax)
    x_minmin = min(x_min, x_minmin)
    y_minmin = min(y_min, y_minmin)

    x_coord = np.linspace(x_min, x_max, 300)
    y_coord = np.linspace(y_min, y_max, 300)
    X_coord, Y_coord = np.meshgrid(x_coord, y_coord)
    Z_coord = xx[0] * X_coord ** 2 + xx[1] * X_coord * Y_coord + xx[2] * Y_coord**2 + xx[3] * X_coord + xx[4] * Y_coord
    ax.contour(X_coord, Y_coord, Z_coord, levels=[1], colors=(color), linewidths=2)
    # ax.scatter(x, y, color=color, s=0.5)

plt.xlim(x_minmin, x_maxmax)
plt.ylim(y_minmin, y_maxmax)
plt.axis('off')
plt.gca().set_aspect('equal', adjustable='box')

for enu, enum in enumerate(time):
    if enu == 0:
        lines = []
    else:
        length = len(lines)
        for b in range(length):
            l = lines.pop(0)[0]
            l.remove()
            del l
        lines = []




    for i, el in enumerate(objects):
        if el['name'] in ['sun', 'earth', 'moon']:
            obj = planets[el['name']]
        else:
            obj = planets[f'{el['name']} barycenter']


        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

        color = colors[i%len(colors)]

        loc_now = obj.at(enum).position.km
        rot = fb.ecliptic_frame.rotation_at(enum)
        r = R.from_matrix(rot)
        loc_now = r.apply(loc_now)
        lines.append(ax.plot(loc_now[0], loc_now[1], color=color, marker='o', markersize=10))
        el['posnow'] = loc_now

    

    plt.pause(0.01)



data = pd.DataFrame(objects)

plt.show()
