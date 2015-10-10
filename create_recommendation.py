import pandas as pd
import numpy as np
import data_io as dio

def create_recommendation():

    vdf = pd.read_csv(dio.data_path + 'nnfromdest2.csv')
    vdf.drop(['visit_cnt'], 1, inplace=True)

    pdf = pd.read_csv(dio.data_path + 'prediction.csv')

    ndf = pd.read_csv(dio.data_path + 'name.csv', index_col=0)

    adf = pd.read_csv(dio.data_path + 'addr.csv', index_col=0)
    adf.drop(['lat', 'lon'], 1, inplace=True)

    mdf = vdf.merge(pdf, on='sigungu_no')
    mdf = mdf.merge(ndf, on='name_no')
    mdf = mdf.merge(adf, on='sigungu_no')


    mdf['year'] = mdf['year'].apply(lambda y: y*(2015-2006)+2006)
    mdf['price'] = mdf['price'].apply(lambda y: y*50000)
    mdf['expense'] = mdf['expense'].apply(lambda y: y*200)

    mdf['rec_rate'] = mdf['rate'] * mdf['prob']

    mdf = mdf.sort(['name_no', 'rec_rate'], ascending=[1, 0])

    #droplist = ['name_no', 'sigungu_no', 'rate', 'prob', 'trade_no']
    droplist = ['name_no', 'year', 'month', 'price', 'expense', 'sigungu_no', 'rate', 'prob', 'trade_no']
    mdf.drop(droplist, 1, inplace=True)

    #reorder = ['name', 'year', 'month', 'price', 'expense', 'sigungu', 'rec_rate']
    reorder = ['name', 'sigungu', 'rec_rate']
    mdf = mdf.reindex(columns=reorder)

    mdf = mdf.drop_duplicates()

    mdf = mdf.groupby(['name', 'sigungu']).sum()

    mdf.to_csv(dio.data_path + 'recommendation.csv')
    mdf = pd.read_csv(dio.data_path + 'recommendation.csv')
    mdf = mdf.sort(['name', 'rec_rate'], ascending=[1, 0])
    mdf.to_csv(dio.data_path + 'recommendation.csv', index=False)




create_recommendation()