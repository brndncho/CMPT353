import sys
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import pykalman as pk

def get_data(filename1):

    lon_list = []
    lat_list = []
    tree = ET.parse(filename1)
    root = tree.getroot()

    for trkpt in root.iter('{http://www.topografix.com/GPX/1/0}trkpt'):
        lat = float(trkpt.attrib['lat'])
        lon = float(trkpt.attrib['lon'])
        lon_list.append(lon)
        lat_list.append(lat)

    df = pd.DataFrame({'lat': lat_list, 'lon': lon_list})
    return df    

# source: https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206 Author: Salvador Dali
def haversine(lat1, lon1, lat2, lon2):

    r = 6371000
    p = 0.017453292519943295

    a = 0.5 - np.cos((lat2-lat1)*p)/2 + np.cos(lat1*p) * np.cos(lat2*p) * (1-np.cos((lon2-lon1)*p))/2
    return 2 * r * np.arcsin(np.sqrt(a))

# source: https://stackoverflow.com/questions/40452759/pandas-latitude-longitude-to-distance-between-successive-rows
def distance(points):
    distance_df = pd.DataFrame(columns=['dist'])
    distance_df['dist'] = \
    haversine(points.lat.shift(1), points.lon.shift(1),
                 points.loc[1:, 'lat'], points.loc[1:, 'lon'])
    distance = distance_df['dist'].sum()
    return distance

def smooth(points):
    kf = pk.KalmanFilter(
        initial_state_mean= points.iloc[0],
        observation_covariance= np.diag([0.3, 0.3]) ** 2,
        transition_covariance= np.diag([0.1, 0.1]) ** 2,
        transition_matrices= [[1, 0], [0, 1]]
    )
    kalman_smoothed, _ = kf.smooth(points)
    df2 = pd.DataFrame(data=kalman_smoothed, columns=['lat', 'lon'])
    return df2

def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')


def main():
    points = get_data(sys.argv[1])
    print('Unfiltered distance: %0.2f' % (distance(points),))
    
    smoothed_points = smooth(points)
    print('Filtered distance: %0.2f' % (distance(smoothed_points),))
    output_gpx(smoothed_points, 'out.gpx')


if __name__ == '__main__':
    main()