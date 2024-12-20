from skyfield.api import load
from skyfield.framelib import ecliptic_frame

ts = load.timescale()
t = ts.utc(2019, 12, 9, 15, 36)

eph = load('de440.bsp')
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

e = earth.at(t)
s = e.observe(sun).apparent()
m = e.observe(moon).apparent()

_, slon, _ = s.frame_latlon(ecliptic_frame)
_, mlon, _ = m.frame_latlon(ecliptic_frame)
phase = (mlon.degrees - slon.degrees) % 360.0

percent = 100.0 * m.fraction_illuminated(sun)

print('Phase (0°–360°): {0:.1f}'.format(phase))
print('Percent illuminated: {0:.1f}%'.format(percent))