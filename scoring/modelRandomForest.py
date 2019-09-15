# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 12:24:48 2019
@author: Ramin

Model check the DAFOLT for Loan. Is Loan in DEFOLT (YES/NO)
Correct model , Accuracy = 100%
"""

import cx_Oracle
import pandas as pd


connstr='xxxxxx'
connection = cx_Oracle.connect(connstr)
query = """SELECT * FROM V_ML_LOAN_PORTFOLIO_TRAIN T"""
dataset = pd.read_sql(query, con=connection)
connection.close

dataset = dataset.loc[dataset['REQ_PERIOD'] >= 6]
dataset = dataset.loc[dataset['JOB_INCOME'] > 0]
dataset = dataset.loc[dataset['REQ_AMOUNT'] <= 20000]
dataset = dataset.loc[dataset['REQ_AMOUNT'] >= 1000]


X = dataset.iloc[:, 0:21].values
y = dataset.iloc[:, 21].values
X_train = X
y_train = y

# Fitting RandomForestClassifier  to the Training set
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 10, random_state = 0)
classifier.fit(X_train, y_train)

from sklearn.externals import joblib
import datetime
now = datetime.datetime.now()
filename = 'modelRandomForest_'+now.strftime("%Y%m%d")+'.sav'
joblib.dump(classifier, filename)
