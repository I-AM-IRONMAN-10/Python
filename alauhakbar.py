from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.const import SUN, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN, NORTH_NODE, SOUTH_NODE
from flatlib import const

# Set ayanamsa to Lahiri (sidereal)
const.AYANAMSA = const.AYANAMSA_LAHIRI

# Use Whole Sign houses for Vedic style
houseSystem = 'W'  # 'W' for Whole Sign, 'S' for Sripati, 'P' for Placidus (Western default)

# Birth details Chennai
date = Datetime('10/11/2005', '16:30', '+05:30')
pos = GeoPos('13:04', '80:17')  # Chennai

# Objects to include
objects = [SUN, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN, NORTH_NODE, SOUTH_NODE]

# Create chart with Vedic settings
chart = Chart(date, pos, IDs=objects, houses=houseSystem)

# Print planets with sidereal sign and house
for obj in objects:
    planet = chart.get(obj)
    house = chart.houses.getHouseByLon(planet.lon)
    print(f"{obj}: {planet.sign} {planet.lon:.2f}° (House {house.num()})")
