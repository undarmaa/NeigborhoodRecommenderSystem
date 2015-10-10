import data_io
import data_io as dio
from datetime import datetime
import pandas as pd

path = dio.data_path
def main():
    testset = pd.read_csv(path + "test_x.csv", index_col=0)

    ## deal with the NAs, and add features
    #train.feature_eng(test)

    ## predict
    print "Loading the predict_model classifier.."
    tstart = datetime.now()

    classifier = data_io.load_model("predict_model")
    print "Time used", datetime.now() - tstart

    print "Making predictions on the predict_model"
    tstart = datetime.now()
    fnames = ['year', 'month', 'trade_no', 'sigungu_no', 'price', 'monthly_expense']
    test_f = testset[fnames].values
    predic_proba = classifier.predict_proba(test_f)[:,1]

    print "Time used", datetime.now() - tstart

    ## Making prediction
    prediction = zip(testset['year'],
                        testset['month'],
                        testset['trade_no'],
                        testset['sigungu_no'],
                        testset['price'],
                        testset['monthly_expense'],
                        predic_proba)

    print "Writing predictions to file.."
    tstart = datetime.now()
    data_io.write_submission(prediction)
    print "Time used,", datetime.now() - tstart

if __name__=="__main__":
    main()

