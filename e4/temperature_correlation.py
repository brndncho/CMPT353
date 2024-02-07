import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# C:/Users/brand/anaconda3/python.exe temperature_correlation.py stations.json.gz city_data.csv output.svg

stations_file = sys.argv[1]
city_data_file = sys.argv[2]
output_file = sys.argv[3]

stations = pd.read_json(stations_file, lines=True)
city_data = pd.read_csv(city_data_file)

stations['avg_tmax'] = stations['avg_tmax'] / 10 # change tmax to C
city_data = city_data.dropna() # drop cities with missing data
city_data['area'] = city_data['area'] / (10**6) # m to km is 10^-6
city_data['density'] = city_data['population'] / city_data['area']
#print(stations)
#print(city_data)

# source: https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206 
# taken from my assignment 3
def distance(city, stations):

    lat1 = city['latitude']
    lon1 = city['longitude']
    lat2 = stations['latitude']
    lon2 = stations['longitude']

    r = 6371000
    p = 0.017453292519943295

    a = 0.5 - np.cos((lat2-lat1)*p)/2 + np.cos(lat1*p) * np.cos(lat2*p) * (1-np.cos((lon2-lon1)*p))/2
    return 2 * r * np.arcsin(np.sqrt(a))


def best_tmax(city, stations):

    station_distance = distance(city, stations)
    closest_station = station_distance.idxmin()
    return stations.loc[closest_station, 'avg_tmax'] # find row with the closest station and take the temperature

city_data['avg_tmax'] = city_data.apply(best_tmax, stations=stations, axis=1)
print(city_data)

plt.scatter(city_data['avg_tmax'], city_data['density'])
plt.title('Temperature vs Population Density')
plt.xlabel('Avg Max Temperature (\u00b0C)')
plt.ylabel('Population Density (people/km\u00b2)')
#plt.show()
plt.savefig(output_file)
