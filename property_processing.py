# -*- coding: utf-8 -*-

"""

    1. python property_processing create_property2
    2. python property_processing create_address_table
    3. python property_processing join_property2_address

"""
import pandas as pd
import numpy as np
import geo
import data_io as dio
from datetime import datetime


#dio.data_path  #"C:\Users\Park\Desktop\data\\"

def create_property2():

    print "create property2"

    tstart = datetime.now()

    df = pd.read_csv(dio.data_path + "property.csv", index_col=0)

    # filtering for region == Seoul
    df = df[df['region'] == u'서울'.encode('cp949')]
    #df = df[(df['region'] == u'서울'.encode('cp949')) | (df['region'] == u'경기'.encode('cp949'))]

    # remove unnecessary feature
    unnec_feature = ['day', 'property_type', 'region', 'bonbun',
                     'bubun', 'complex_name', 'road_name', 'gross_area',
                     'lot_area', 'use_area', 'floor', 'build_year']

    df = df.drop(unnec_feature, 1)

    # strip empty spaces in address
    df['sigungu'] = df['sigungu'].map(str.strip)

    # fill N/A values
    df['price'].fillna(0, inplace=True)
    df['monthly_expense'].fillna(0, inplace=True)

    # add new feature = 'trade_no', 'sigungu_no', 'lat', 'lon'
    df['trade_no'] = 0

    trade_type = [u'매매', u'전세', u'월세']
    for i in range(len(trade_type)):
        df.loc[df['trade_type'] == trade_type[i].encode('cp949'), 'trade_no'] = i

    df = df.drop('trade_type', 1)

    df.to_csv(dio.data_path + "property2.csv")

    print "save " + dio.data_path + "property2.csv"
    print datetime.now() - tstart
    return df


def create_address_table():

    print "create address table"
    tstart = datetime.now()

    df = pd.read_csv(dio.data_path + "property2.csv", index_col=0)

    # create mapping table for address
    addr = pd.DataFrame(columns=['sigungu'])
    addr['sigungu'] = df['sigungu'].copy(True)
    addr = addr.drop_duplicates()
    addr['sigungu_no'] = range(0, addr.shape[0])
    addr = addr.set_index('sigungu_no')

    addr_df = pd.DataFrame(columns=['sigungu_no', 'sigungu', 'lat', 'lon'])

    for i in range(addr.shape[0]):
        address = addr['sigungu'][i].decode('cp949')
        lat, lon, err = geo.getGeocoordFromAddr(address)

        if err == False:
            addr_df.loc[i] = [i, addr['sigungu'][i], lat, lon]
            # addr.loc[i]['lat'] = float(lat)   error
            # addr.loc[i]['lon'] = float(lon)
            #print addr_df.loc[i]
            print i, address, lat, lon
        else:
            #addr_df.loc[i] = [i, addr['sigungu'][i], 0, 0]
            print i, address, "Err"

    addr_df.to_csv(dio.data_path + "addr.csv")

    print datetime.now() - tstart
    return addr_df


def join_property2_address():
    print "join property2 and address table"
    tstart = datetime.now()

    prop = pd.read_csv(dio.data_path + "property2.csv", index_col=0)
    addr = pd.read_csv(dio.data_path + "addr.csv", index_col=0)
    jdf = prop.merge(addr, on='sigungu')
    jdf = jdf.drop('sigungu', 1)

    jdf.to_csv(dio.data_path + "property3.csv")

    print datetime.now() - tstart



    # mapping feature
    # rs = len(region)
    # for i in range(rs):
    #     df.loc[df['region'] == region[i].encode('cp949'),'region2'] = i/(rs-1.)
    #
    # print df['region2']

    # addr = pd.read_csv(path + "addr.csv")
    # rs = addr.shape[0]
    # print rs
    # for i in range(rs):
    #     #df.loc[df['sigungu'] == addr['address'][i], 'sigungu2'] = i/(rs-1.)
    #


""" property3.csv -> trainSet(prop_summary) """
def summarize_property3():
    print "summarize property3 to summary"
    tstart = datetime.now()

    df = pd.read_csv(dio.data_path + "property3.csv", index_col=0)

    df = df.drop(['lat', 'lon'], 1)
    df = df[df.price != '##########']
    # df['year'] = df['year'].astype(float)
    # ymax = df['year'].max()
    # ymin = df['year'].min()
    # df['year'] = df['year'].apply(lambda y: (y-ymin)/(ymax-ymin))

    df['year'] = df['year'].astype(float)

    df['price'] = df['price'].str.replace(',', '')
    df['price'] = df['price'].astype(float)
    df['price'].fillna(0, inplace=True)

    df['monthly_expense'] = df['monthly_expense'].str.replace(',', '')
    df['monthly_expense'] = df['monthly_expense'].astype(float)
    df['monthly_expense'].fillna(0, inplace=True)

    df = df[(df.price <= 50000) & (df.monthly_expense <= 200)]

    df['price_for_group'] = df['price']
    df.loc[df['price_for_group'] == 0, 'price_for_group'] = 1
    df['group_price'] = pd.cut(df['price_for_group'], np.arange(0, 50500, 500), labels=np.arange(0, 50000, 500))
    df['group_price'] = df['group_price'].astype(float)

    df['exp_for_group'] = df['monthly_expense']
    df.loc[df['exp_for_group'] == 0, 'exp_for_group'] = 1
    df['group_exp'] = pd.cut(df['exp_for_group'], np.arange(0, 210, 10), labels=np.arange(0, 200, 10))
    df['group_exp'] = df['group_exp'].astype(float)

    df['year'] = normalize_column(df['year'])
    #df['price'] = normalize_column(df['price'])
    df['group_price'] = normalize_column(df['group_price'])
    #df['monthly_expense'] = normalize_column(df['monthly_expense'])
    df['group_exp'] = normalize_column(df['group_exp'])

    gb = df.groupby(['year', 'month', 'trade_no', 'sigungu_no', 'group_price', 'group_exp'])

    summary = gb.size()
    type(summary)
    summary.to_csv(dio.data_path + "prop_summary.csv")
    print datetime.now() - tstart

def createTrainSet():
    summary = pd.read_csv(dio.data_path + "prop_summary.csv", index_col=False, header=None)
    summary.columns = ['year', 'month', 'trade_no', 'sigungu_no', 'price', 'exp', 'count']

    summary['count'] = normalize_column(summary['count'])

    summary.to_csv(dio.data_path + "train_set.csv", header=False, index=False)
    #summary[:][:-1].to_csv(dio.data_path + "train_x.csv")
    #summary[:][-1:].to_csv(dio.data_path + "train_y.csv")

    #
    # #df = df.sort(columns='monthly_expense', ascending=False)
    # df.to_csv(dio.data_path + "trainSet.csv")
    #print df[:5]



def figureCorrelationPlot(df):
    import matplotlib.pyplot as plt
    covmat = df.corr()
    fig = plt.figure().add_subplot(111)
    plt.pcolor(covmat)
    plt.colorbar()
    fig.set_xticklabels(df.columns)
    fig.set_yticklabels(df.columns)
    plt.show()


def normalize_column(col, ymin=0, ymax=0):
    col = col.astype(float)
    if ymax == 0 and ymin == 0:
        ymax = col.max()
        ymin = col.min()
    print ymax, ymin
    col = col.apply(lambda y: (y-ymin)/(ymax-ymin))

    return col


import sys
if __name__ == "__main__":
    pass
    # if len(sys.argv) < 2:
    #         print(__doc__)
    # else:
    #     func = globals()[sys.argv[1]]
        #func(*sys.argv[2:])

    # df = create_property2()
    # addr = create_address_table()
    # join_property2_address()

    #summarize_property3()
    #createTrainSet()
