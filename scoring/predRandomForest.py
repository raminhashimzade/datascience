# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 12:24:48 2019
@author: Ramin

Model check the DAFOLT for Loan. Is Loan in DEFOLT (YES/NO)
Correct model , Accuracy = 100%
"""

import cx_Oracle
import pandas as pd
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)


connstr='xxxxxxxx'
connection = cx_Oracle.connect(connstr)
queryPred = """select * from V_ML_LOAN_PORTFOLIO_PRED t where t.GL_ID = 1012488"""
datasetPred = pd.read_sql(queryPred, con=connection)
connection.close

X_test = datasetPred.iloc[:, 0:21].values

from sklearn.externals import joblib
filename = 'modelRandomForest_20190430.sav'
loaded_model = joblib.load(filename)
y_pred = loaded_model.predict(X_test)


print(y_pred)
