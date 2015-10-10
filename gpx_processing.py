from os import listdir
from pygpx import GPX
import pandas as pd
import data_io as dio
from numpy import *
from datetime import datetime

path = dio.data_path #"C:\Users\Park\Desktop\data\\"

""" Many GPX -> Track_Destination.csv, name.csv """
def extract_destination_and_name():

    print "start extract destination and name"
    tstart = datetime.now()

    data_dir = ".\\gpx"
    folderList = listdir(data_dir)

    df = pd.DataFrame(columns=('name_no', 'time', 'lat', 'lon'))

    name_df = pd.DataFrame(columns=('name_no', 'name'))

    idx = 0

    def inRange(lat, lon):
        if (37.2 <= lat <= 37.7) and (126.7 <= lon <= 127.2):
            return True
        else:
            return False

    for i in range(len(folderList)):
        name_df.loc[i] = [i, folderList[i]]
        dataList = listdir(data_dir + "\\" + folderList[i])
        for j in range(len(dataList)):
            filepath = data_dir + "\\" + folderList[i] + "\\" + dataList[j]
            try:
                print filepath
                gpx = GPX(filepath)
            except:
                print 'ignored', filepath
                continue

            tracks = gpx.tracks
            track = tracks[0]

            start_time = track.start_time()
            end_time = track.end_time()

            start_pt = track.start()
            end_pt = track.end()

            #full_duration = track.full_duration()
            #distance = track.distance()

            if inRange(start_pt.lat, start_pt.lon):
                df.loc[idx] = [i, start_time, start_pt.lat, start_pt.lon]
                idx += 1

            if inRange(end_pt.lat, end_pt.lon):
                df.loc[idx] = [i, end_time, end_pt.lat, end_pt.lon]
                idx += 1

    print idx

    df.to_csv(path + "dest.csv")
    name_df.to_csv(path + "name.csv")
    print "save " + path + "dest.csv"
    print "save " + path + "name.csv"
    print datetime.now() - tstart

def plot_destination(filter=""):
    # name filter = [HD, KSY, Park, undaraa, ... ]

    df = pd.read_csv(path + "dest.csv")

    # min = ts.apply(lambda x: x.min())
    # xmin = min['lon']
    # max = ts.apply(lambda x: x.max())
    # xmax = max['lon']
    # print xmin, xmax

    if filter != "":
        df = df[df['name_no'] == int(filter)]

    # show the figure for destination
    # x axis : longitude
    # y axis : latitude
    ax = df.plot(kind="scatter", x='lon', y='lat',
                 color="DarkBlue", label='Destinations', s=5)

    #ax.set_xticks(np.arange(126.7, 127.2, 0.1))
    ax.axis([126.7, 127.2, 37.2, 37.7])

    # show the figure for hongik university
    hongikuniv = pd.DataFrame(columns=['name', 'lat','lon'])
    hongikuniv.loc[0] = ['Hongik Univ', 37.550136, 126.924685]
    hongikuniv.plot(kind="scatter", x='lon', y='lat',
                    color="Red", s=20, label='Hongik University', ax=ax)



#extract_destination_and_name()
plot_destination('0')