import csv
from operator import itemgetter
import os
import json
import pickle
import pandas as pd
from datetime import datetime


data_path = ".\data\\"

def get_paths():
    paths = json.loads(open("SETTINGS.json").read())
    for key in paths:
        paths[key] = os.path.expandvars(paths[key])
    return paths

def read_csv(path):
    print "Reading '%s' data..." % path
    tstart = datetime.now()

    df = pd.read_csv(path)

    # print the time interval
    print "Time used,", datetime.now() - tstart

    return df


def save_model(model, model_name): #, latlon):
    path = get_paths()[model_name]
    pickle.dump(model, open(path, "w"))


def load_model(model_name):
    path = get_paths()[model_name]
    return pickle.load(open(path))


def write_submission(recommendations):

    submission_path = get_paths()["prediction_path"]

    rows = [(year, month, trade_no, sigungu_no, price, expense, prob)
        for year, month, trade_no, sigungu_no, price, expense, prob
        in sorted(recommendations, key=itemgetter(6),reverse=True)]

    writer = csv.writer(open(submission_path, "w"), lineterminator="\n")
    writer.writerow(('year', 'month', 'trade_no', 'sigungu_no', 'price', 'expense', 'prob'))
    writer.writerows(rows)
