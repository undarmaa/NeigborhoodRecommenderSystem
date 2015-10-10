import sys
import data_io
import model
import pandas as pd
import random
from datetime import datetime


def get_features():
    feature_names = ['name_no', 'time']

    # if "comp1_rate" in feature_names:
    #     ## only true in the test set
    #     feature_names.remove("comp1_rate")
    #
    # feature_names.remove("visitor_hist_starrating")
    # feature_names.append("comp_inv_sum")
    return feature_names


def feature_eng(train):

    ## deal with NAs in hotels's infor
    train['prop_review_score'].fillna(3, inplace=True)
    train['prop_review_score'][train['prop_review_score']==0]=2.5
    train["prop_location_score2"].fillna(0, inplace=True)
    avg_srch_score = train["srch_query_affinity_score"].mean()
    train["srch_query_affinity_score"].fillna(avg_srch_score, inplace=True)
    train["orig_destination_distance"].fillna(1509,inplace=True)
    train["visitor_hist_adr_usd"].fillna(0, inplace=True)
    train['visitor_hist_starrating_bool'] = pd.notnull(train['visitor_hist_starrating'])

    ## add feature: comp_rate_sum
    for i in range(1,9):
        train['comp'+str(i)+'_rate'].fillna(0, inplace=True)

    train['comp_rate_sum'] = train['comp1_rate']
    for i in range(2,9):
        train['comp_rate_sum'] += train['comp'+str(i)+'_rate']

    ## add feature: comp_rate_sum
    for i in range(1,9):
        train['comp'+str(i)+'_inv'].fillna(0, inplace=True)
        train['comp'+str(i)+'_inv'][train['comp'+str(i)+'_inv']==1] = 10
        train['comp'+str(i)+'_inv'][train['comp'+str(i)+'_inv']==-1] = 1
        train['comp'+str(i)+'_inv'][train['comp'+str(i)+'_inv']==0] = -1
        train['comp'+str(i)+'_inv'][train['comp'+str(i)+'_inv']==10] = 0
    train['comp_inv_sum'] = train['comp1_inv']
    for i in range(2,9):
        train['comp_inv_sum'] += train['comp'+str(i)+'_inv']

def main():

    #sample_size = int(sys.argv[1])
    ## sample_size = int(1000)

    # read train.csv
    train = pd.read_csv(data_io.data_path + "train_set.csv", index_col=False, header=None)
    train.columns = ['year', 'month', 'trade_no', 'sigungu_no', 'price', 'expense', 'count']
    print "Data Size:", (train.shape)

    # feature engineering
    #feature_eng(train)

    ## originally sample size = 100000
    train = train[:300000]

    #
    # book_trainset = train_set[train_set['booking_bool']==1]
    # book_rows = book_trainset.index.tolist()
    # bsize = len(book_trainset.index)
    # click_trainset = train_set[train_set['click_bool']==1]
    # click_rows = click_trainset.index.tolist()
    # csize = len(click_trainset.index)
    # print 'bsize ' + str(bsize)
    # print 'csize ' + str(csize)
    # book_trainset = book_trainset.append(train_set.ix[random.sample(train_set.drop(book_rows).index, bsize)])
    # click_trainset =click_trainset.append(train_set.ix[random.sample(train_set.drop(click_rows).index, csize)])

    #book_trainset = train_set.ix[random.sample(train_set.drop(book_rows).index, bsize)]


    model_name = "predict_model"
    response_name = 'count'
    feature_names = ['year', 'month', 'trade_no', 'sigungu_no', 'price', 'expense'] #get_features()

    print "Training the " + model_name + " Classifier..."
    print "Using " + str(len(feature_names)) + " features..."
    tstart = datetime.now()

    features = train[feature_names].values
    target = train[response_name].values

    classifier = model.model()
    classifier.fit(features, target)

    print "Time used,", datetime.now() - tstart

    print "Saving the classifier..."
    tstart = datetime.now()
    data_io.save_model(classifier, model_name)
    print "Time used,", datetime.now() - tstart

if __name__=="__main__":
    main()
