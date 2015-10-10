# -*- coding: utf-8 -*-

"""
    python utils.py function_name

"""
from numpy import *
import numpy as np
from os import listdir
import os
import pandas as pd
import csv


"""
def merge_csv(data_dir, mergedname, save_dir="C:\Users\Park\Desktop\\"):

    dataList = listdir(data_dir)

    datacnt = len(dataList)
    print datacnt

    mergeddata = pd.DataFrame()
    for i in range(datacnt):
        loc_data = pd.read_csv(data_dir + "\\" + dataList[i])
        #os.remove(data_dir + "\\" + dataList[i])
        print loc_data.shape, " ", dataList[i]
        mergeddata = mergeddata.append(loc_data)

    print mergeddata.shape
    #
    mergeddata.to_csv(save_dir + mergedname)
"""

from math import sin, cos, sqrt, atan2, radians

def getDistanceBetweenLatLon(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

import datetime, dateutil.parser
import geo
import geopy


"""
def coordtoadd():
    tta = pd.read_csv("C:\Users\Park\Desktop\data\\track_train_addr.csv")
    rs = tta.shape[0]
    for i in range(rs):

        addr = geo.getAddrFromGeocoord(tta['lat'][i], tta['lon'][i])


        #addrstr = " ".join(addr)
        print i, addr
        tta['addr'].loc[i] = addr.encode('cp949')

    tta.to_csv("C:\Users\Park\Desktop\data\\track_train_addr2.csv")
"""


import sys
if __name__ == "__main__":
    pass
    # if len(sys.argv) < 2:
    #         print(__doc__)
    # else:
    #     func = globals()[sys.argv[1]]
    #     func(*sys.argv[2:])

    # version = 5
    #
    # #coordtoadd()
