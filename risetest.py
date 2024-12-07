from skyfield import almanac
from skyfield.api import N, S, E, W, load, wgs84
import datetime
import matplotlib.pyplot as plt
import math

ts = load.timescale()
eph = load('de440.bsp')
sun = eph['Sun']
bluffton = wgs84.latlon(52.2338172 * N, 6.9183279 * W)
observer = eph['Earth'] + bluffton

t0 = ts.now()
t1 = t0 + 1

t, y = almanac.find_risings(observer, sun, t0, t1)
# print(t.utc_iso(' '))

t, y = almanac.find_settings(observer, sun, t0, t1)
# print(t.utc_iso(' '))

moon = eph['Moon']

t, y = almanac.find_risings(observer, moon, t0, t1)
# print('Moonrises (UTC):', t.utc_iso(' '))

t, y = almanac.find_settings(observer, moon, t0, t1)#
time = t.utc_datetime()[0]
# print(time.hour)
# print('Moonsets (UTC):', t.utc_datetime())
if time.hour > 12:
    a = time.hour - 12
else:
    a = time.hour

b =  a + time.minute/60 + time.second/3600

b=3

angle = -((b/12 * math.pi)*2) + math.pi/2

x = math.cos(angle)
print(x)
y = math.sin(angle)

img = plt.imread('clock.png')
fig, ax = plt.subplots()
ax.imshow(img, extent=[-1, 1, -1, 1])
plt.plot(x, y, 'ro')
plt.xlim(-1, 1)
plt.ylim(-1, 1)

plt.show()
