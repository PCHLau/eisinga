from skyfield.api import load
import skyfield.framelib as fb
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R
import scipy.optimize
import functools

ts = load.timescale()
t = ts.now()

planets = load('de440.bsp')

objects = ['sun', 'earth', 'moon', 'mercury', 'venus', 'mars',
           'jupiter', 'saturn'
           ,'uranus', 'neptune', 'pluto'
           ]

new_data = []
points = []

for i, el in enumerate(objects):
    if objects[i] in ['sun', 'earth', 'moon']:
        obj = planets[objects[i]]
        print(obj)
    else:
        obj = planets[f'{objects[i]} barycenter']
    
    location = obj.at(t).position.km

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

    color = colors[i%len(colors)]

    rot = fb.ecliptic_frame.rotation_at(t)
    r = R.from_matrix(rot)

    location = r.apply(location)
    
    new_data.append({'name': objects[i], 'x': location[0], 'y': location[1], 'z': location[2], 'color': color})
    points.append((location[0], location[1], location[2]))

def plane(x, y, params):
    a = params[0]
    b = params[1]
    c = params[2]
    z = a*x + b*y + c
    return z

def error(params, points):
    result = 0
    for (x,y,z) in points:
        plane_z = plane(x, y, params)
        diff = abs(plane_z - z)
        result += diff**2
    return result

def cross(a, b):
    return [a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0]]

fun = functools.partial(error, points=points)
params0 = [0.5, 0.5, 0.5]
res = scipy.optimize.minimize(fun, params0, method='Nelder-Mead')

print(res)

a = res.x[0]
b = res.x[1]
c = res.x[2]

xs, ys, zs = zip(*points)

fig = plt.figure()

ax = plt.axes(projection='3d')

ax.scatter(xs, ys, zs)

point  = np.array([0.0, 0.0, c])
normal = np.array(cross([1,0,a], [0,1,b]))
print(point)
print(normal)
angle = np.arccos(np.dot(normal, [0,0,1])/(np.linalg.norm(normal)*np.linalg.norm([0,0,1])))
print(angle*180/np.pi)
d = -point.dot(normal)
xx, yy = np.meshgrid([-1000000000,1000000000], [-1000000000,1000000000])
z = (-normal[0] * xx - normal[1] * yy - d) * 1. /normal[2]
ax.plot_surface(xx, yy, z, alpha=0.2, color=[0,1,0])

data = pd.DataFrame(new_data)

# print(data)

# fig = plt.figure()

# ax = plt.axes(projection='3d')

# ax.scatter(data['x'], data['y'], data['z'], color=data['color'])

plt.show()