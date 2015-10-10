# -*- coding: utf-8 -*-

import pandas as pd
import data_io as dio
from datetime import date
from datetime import datetime
from datetime import timedelta

def normalize_column(col, ymin=0, ymax=0):
    if ymax == 0 and ymin == 0:
        ymax = col.max()
        ymin = col.min()
    print ymax, ymin
    col = col.astype(float)
    col = col.apply(lambda y: (y-ymin)/(ymax-ymin))

    return col

#trade_no = raw_input(u'거래 유형 입력(0 - 매매, 1 - 전세, 2 - 월세) : ')
deposit = raw_input(u'매매/보증금 입력 : ')

mexp = 0

#if trade_no != '0':
mexp = raw_input(u'월세 입력 : ')

init_deposit = 0
stop_deposit = int(deposit)

init_mexp = 0
stop_mexp = int(mexp)

df = pd.DataFrame(columns=['year', 'month', 'price', 'monthly_expense', 'trade_no', 'sigungu_no'])
addr = pd.read_csv(dio.data_path + "addr.csv", index_col=0)

addrmax = addr['sigungu_no'].max()

addrmax = int(addrmax.astype(int))

print "generate test set"
tstart = datetime.now()

i = 0
rng = 3

for s in range(addrmax):
    d = date(date.today().year, date.today().month, 1)

    for r in range(rng):       # year, month

        year = d.year
        month = d.month

        for t in range(3):        # trade_no
            for j in range(init_deposit, stop_deposit, 500):
                if t == 0:
                    df.loc[i] = [year, month, j, 0., t, s]
                    #print i, df[i]
                    i += 1
                else:
                    for l in range(init_mexp, stop_mexp, 10):
                        df.loc[i] = [year, month, j, l, t, s]
                        #print i, df[i]
                        i += 1

        d = d + timedelta(days=31)


df['year'] = normalize_column(df['year'], 2006, 2015)
df['price'] = normalize_column(df['price'], 0, 50000)
df['monthly_expense'] = normalize_column(df['monthly_expense'], 0, 200)

print datetime.now() - tstart

df.to_csv(dio.data_path + 'test_x.csv')