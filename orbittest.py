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
t = ts.now()

time=[]

today = datetime.datetime(2024, 1, 1, tzinfo=utc)

for i in range(1,100):
    time.append(ts.from_datetime(today))
    today += datetime.timedelta(days=1000)

planets = load('de440.bsp')

objects = ['sun', 'earth'
           , 'moon', 'mercury', 'venus', 'mars'
        #  , 'jupiter', 'saturn'
           ,'uranus', 'neptune', 'pluto'
           ]

new_data = []

for i, el in enumerate(objects):
    if el in ['sun', 'earth', 'moon']:
        obj = planets[objects[i]]
    else:
        obj = planets[f'{objects[i]} barycenter']

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

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

    new_data.append({'name': objects[i], 'x': x, 'y': y, 'z': z, 'color': color})

fig = plt.figure()

data = pd.DataFrame(new_data)

X = np.array([[data['x'][8][0]]])
Y = np.array([[data['y'][8][0]]])

for i, a in enumerate(data['x'][1]):
    if i == 0:
        continue
    X = np.append(X, [[data['x'][8][i]]], axis=0)
    Y = np.append(Y, [[data['y'][8][i]]], axis=0)

A = np.hstack([X**2, X * Y, Y**2, X, Y])
b = np.ones_like(X)
x = np.linalg.lstsq(A, b)[0].squeeze()

print(x)



for i in range(len(data)):
    plt.scatter(data['x'][i], data['y'][i], color=data['color'][i], s=0.5)


print(X.max())
print(X.min())
print(Y.max())
print(Y.min())



x_coord = np.linspace(X.min()+(X.min()/10), X.max()+(X.max()/10), 300)
y_coord = np.linspace(Y.min()+(Y.min()/10), Y.max()+(Y.max()/10), 300)
X_coord, Y_coord = np.meshgrid(x_coord, y_coord)
Z_coord = x[0] * X_coord ** 2 + x[1] * X_coord * Y_coord + x[2] * Y_coord**2 + x[3] * X_coord + x[4] * Y_coord
print(Z_coord)
plt.contour(X_coord, Y_coord, Z_coord, levels=[1], colors=('r'), linewidths=2)

plt.show()