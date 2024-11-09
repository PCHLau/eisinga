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

ts = load.timescale()
t = ts.now()

time=[]

today = datetime.datetime(2024, 1, 1, tzinfo=utc)

for i in range(1,100):
    time.append(ts.from_datetime(today))
    today += datetime.timedelta(days=10)

planets = load('de440.bsp')

objects = ['sun', 'earth'
           , 'moon', 'mercury', 'venus', 'mars',
        #    'jupiter', 'saturn'
        #    ,'uranus', 'neptune', 'pluto'
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

x = np.array(data['x'][1])
y = np.array(data['y'][1])

print(x.max())
print(x.min())
print(y.max())
print(y.min())

N = len(x)

print(N)

xmean, ymean = x.mean(), y.mean()
x -= xmean
y -= ymean
U, S, V = np.linalg.svd(np.stack((x, y)))

tt = np.linspace(0, 2*np.pi, 1000)
circle = np.stack((np.cos(tt), np.sin(tt)))    # unit circle
transform = np.sqrt(2/N) * U.dot(np.diag(S))   # transformation matrix
fit = transform.dot(circle) + np.array([[xmean], [ymean]])
plt.plot(fit[0, :], fit[1, :], 'r')


for i in range(len(data)):
    plt.scatter(data['x'][i], data['y'][i], color=data['color'][i], s=0.5)


plt.show()
