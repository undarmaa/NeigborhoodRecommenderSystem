from sklearn import cross_validation
import data_io as dio

import csv
with open(dio.data_path + 'train_set.csv') as f1:
    next(f1)
    reader = csv.reader(f1, delimiter=',')
    input_set = []
    for row in reader:
        input_set.append(row)


train_set, intermediate_set = cross_validation.train_test_split(input_set, train_size=0.6, test_size=0.4)
valid_set, test_set = cross_validation.train_test_split(intermediate_set, train_size=0.5, test_size=0.5)


f = open(dio.data_path + 'train.csv', 'wb')
wr = csv.writer(f, quoting=csv.QUOTE_ALL)
wr.writerows(train_set)
f.close()
print "train"


f = open(dio.data_path + 'valid.csv', 'wb')
wr = csv.writer(f, quoting=csv.QUOTE_ALL)
wr.writerows(valid_set)
f.close()
print "cv"

f = open(dio.data_path + 'test.csv', 'wb')
wr = csv.writer(f, quoting=csv.QUOTE_ALL)
wr.writerows(test_set)
f.close()
print "test"