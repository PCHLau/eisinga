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

ts = load.timescale()
now = ts.now()

time=[]

today = datetime.datetime(2024, 1, 1, tzinfo=utc)

for i in range(1,100):
    time.append(ts.from_datetime(today))
    today += datetime.timedelta(days=1000)

planets = load('de440.bsp')

objects = [{'name': 'sun', 'orbper': None}
            ,{'name': 'earth', 'orbper': 365.256363004}
            ,{'name': 'moon', 'orbper': 365.256363004}
            ,{'name': 'mercury', 'orbper': 87.9691}
            ,{'name': 'venus', 'orbper':224.701}
            ,{'name': 'mars', 'orbper': 686.980}
            ,{'name': 'jupiter', 'orbper': 4332.59}
            ,{'name': 'saturn', 'orbper': 10755.70}
            # ,{'name': 'uranus', 'orbper': 30688.5}
            # ,{'name': 'neptune', 'orbper': 60195}
            # ,{'name': 'pluto', 'orbper': 90560}
           ]

new_data = []

fig = plt.figure()

x_max = 0
y_max = 0
x_min = 0
y_min = 0

for i, el in enumerate(objects):
    if el['name'] in ['sun', 'earth', 'moon']:
        obj = planets[el['name']]
    else:
        obj = planets[f'{el['name']} barycenter']


    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    color = colors[i%len(colors)]

    loc = []

    for j, t in enumerate(time):
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

    x_coord = np.linspace(x_min, x_max, 300)
    y_coord = np.linspace(y_min, y_max, 300)
    X_coord, Y_coord = np.meshgrid(x_coord, y_coord)
    Z_coord = xx[0] * X_coord ** 2 + xx[1] * X_coord * Y_coord + xx[2] * Y_coord**2 + xx[3] * X_coord + xx[4] * Y_coord
    plt.contour(X_coord, Y_coord, Z_coord, levels=[1], colors=(color), linewidths=2)

    loc_now = obj.at(now).position.km
    rot = fb.ecliptic_frame.rotation_at(now)
    r = R.from_matrix(rot)
    loc_now = r.apply(loc_now)
    plt.scatter(loc_now[0], loc_now[1], color=color, s=100)

    el['posnow'] = loc_now

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

data = pd.DataFrame(objects)

plt.show()
