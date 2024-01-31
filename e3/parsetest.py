import sys
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
from math import cos, asin, sqrt, pi

def get_data(file):

    lon_list = []
    lat_list = []
    tree = ET.parse(file)
    root = tree.getroot()

    for trkpt in root.iter('{http://www.topografix.com/GPX/1/0}trkpt'):
        lat = float(trkpt.attrib['lat'])
        lon = float(trkpt.attrib['lon'])
        lon_list.append(lon)
        lat_list.append(lat)

    df = pd.DataFrame({'lat': lat_list, 'lon': lon_list}).astype('float64')
    return df    

def haversine(lat1, lon1, lat2, lon2, to_radians=True, earth_radius=6371):

    r = 63710000
    p = 0.017453292519943295

    a = 0.5 - np.cos((lat2-lat1)*p)/2 + np.cos(lat1*p) * np.cos(lat2*p) * (1-np.cos((lon2-lon1)*p))/2
    return 2 * r * np.arcsin(np.sqrt(a))

def distance(df):
    
    df['dist'] = \
    haversine(df.lat.shift(1), df.lon.shift(1),
                 df.loc[1:, 'lat'], df.loc[1:, 'lon'])
    distance = df['dist'].sum()
    return distance

def main():
    #points = get_data(sys.argv[1])
    #print(points)
    #points_test = points.shift(periods=-1)
    #print(points_test)
    #pointsdiff = abs(points-points_test)
    #print(pointsdiff.sum())
    points = pd.DataFrame({
    'lat': [49.28, 49.26, 49.26],
    'lon': [123.00, 123.10, 123.05]})
    print(distance(points).round(6))
    print(points)



if __name__ == '__main__':
    main()
 