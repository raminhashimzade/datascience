# -*- coding: utf-8 -*-

import cx_Oracle
import pandas as pd
import matplotlib.pyplot as plt

connstr='xxxxxxxx'
connection = cx_Oracle.connect(connstr)
query = """SELECT * FROM V_ML_LOAN_PORTFOLIO_RESULT T"""
dataset = pd.read_sql(query, con=connection)
connection.close

dataset["PRECISION_b"] = (dataset["PRECISION"] == 'True').astype(int)

dataset_3000 = dataset[dataset["GL_MESSAGE_ID"] == 3000]
dataset_3001 = dataset[dataset["GL_MESSAGE_ID"] == 3001]
dataset_3002 = dataset[dataset["GL_MESSAGE_ID"] == 3002]
dataset_3003 = dataset[dataset["GL_MESSAGE_ID"] == 3003]


import seaborn as sns

sns.countplot(y = 'PRECISION_b', data=dataset_3000)

g = sns.FacetGrid(data=dataset, col='GL_MESSAGE_ID', col_wrap=4)
g.map(plt.hist, 'PRECISION_b', bins = 20, color = 'r')
