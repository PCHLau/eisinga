from skyfield import almanac
from skyfield.api import N, S, E, W, load, wgs84
import datetime

ts = load.timescale()
eph = load('de440.bsp')
sun = eph['Sun']
bluffton = wgs84.latlon(52.2338172 * N, 6.9183279 * W)
observer = eph['Earth'] + bluffton

t0 = ts.now()
t1 = t0 + 1

t, y = almanac.find_risings(observer, sun, t0, t1)
print(t.utc_iso(' '))

t, y = almanac.find_settings(observer, sun, t0, t1)
print(t.utc_iso(' '))

moon = eph['Moon']

t, y = almanac.find_risings(observer, moon, t0, t1)
print('Moonrises (UTC):', t.utc_iso(' '))

t, y = almanac.find_settings(observer, moon, t0, t1)
print('Moonsets (UTC):', t.utc_iso(' '))