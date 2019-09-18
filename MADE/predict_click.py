#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 23:15:48 2019
@author: ramin
"""

def loss(test_v, pred_v):
    from sklearn.metrics import log_loss
    loss = log_loss(test_v, pred_v)
    return loss


import pandas as pd

# loading data
df = pd.read_csv('train.tar.gz', compression='gzip', header=0, sep=';', quotechar='"', nrows=3000000)
df['label'].describe()
df["label"].sum()
df.dtypes
df_backup = df
# df = df_backup

df = df[['label', 'train.csv', 'C1', 'C2', 'C3', 'C4', 'C5', 'C7', 'C8', 'C10', 'l1', 'l2', 'C12']]

# check is null and drop null columns
df.isnull().sum().sort_values()
df.notnull()
df.isnull().values.any()
null_columns=df.columns[df.isnull().any()]
df[null_columns].isnull().sum()
df.columns
df = df.dropna(axis = 1)
df.columns


# heatmap of coorelation
import seaborn as sns
sns.heatmap(df.corr(), annot=True)
corr = df.corr()

# dropping non-informative fields
#df = df.drop('C6', axis = 1)
#df = df.drop('C9', axis = 1)
#df = df.drop('C11', axis = 1)


# analyzing other fields
#c7type = pd.crosstab(index=df["C7"], columns=df["label"])
#c11type = pd.crosstab(index=df["C11"], columns=df["label"])


#df.loc[:, 'C7'].value_counts()
#var = "C7"
#data = pd.concat([df['label'], df[var]], axis=1)
#sns.countplot(x=var, data=data)
#
#df.loc[:, 'C11'].value_counts()
#var = "C11"
#data = pd.concat([df['label'], df[var]], axis=1)
#sns.countplot(x=var, data=data)
#
#df.loc[:, 'C12'].value_counts()
#var = "C12"
#data = pd.concat([df['label'], df[var]], axis=1)
#sns.countplot(x=var, data=data)

###############################################################################
#var = "C1"
#data = pd.concat([df['label'], df[var]], axis=1)
#sns.countplot(x=var, data=data)
#data.loc[:, var].value_counts()
###############################################################################

# setting x,y
X = df.iloc[:, 1:].values
y = df.iloc[:, 0].values

# scaling the data
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X = sc.fit_transform(X)


# split to train and test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 2)

###################################
# using randomforest classification model
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 50, random_state = 0)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
print('Randomforest accuracy:', accuracy_score(y_pred, y_test))
print('')
print('Confusion matrix:')
print(confusion_matrix(y_test,y_pred))
print('logloss = ' + str(loss(y_test, y_pred)))


###################################
# using LogisticRegression model
from sklearn.linear_model import LogisticRegression
model_1 = LogisticRegression()
model_1.fit(X_train, y_train)
y_pred = model_1.predict(X_test)

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
print('LogisticRegression accuracy:', accuracy_score(y_pred, y_test))
print('')
print('Confusion matrix:')
print(confusion_matrix(y_test,y_pred))
print('logloss = ' + str(loss(y_test, y_pred)))


###################################
# using DecisionTreeClassifier model
from sklearn.tree import DecisionTreeClassifier
model_2 = DecisionTreeClassifier()
model_2.fit(X_train, y_train)
y_pred = model_2.predict(X_test)

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
print('DecisionTreeClassifier accuracy:', accuracy_score(y_pred, y_test))
print('')
print('Confusion matrix:')
print(confusion_matrix(y_test,y_pred))
print('logloss = ' + str(loss(y_test, y_pred)))


##############################################################################
## preparing test data
df_test = pd.read_csv('test-data.tar.gz', compression='gzip', header=0, sep=',', quotechar='"', nrows=1000000)
df_sample = pd.read_csv('sample_submission.csv', nrows=1000000)

df_test.notnull()
df_test.isnull().values.any()
null_columns=df_test.columns[df_test.isnull().any()]
df_test[null_columns].isnull().sum()
df_test.columns
df_test = df_test.dropna(axis = 1)

df_test = df_test.drop('Unnamed: 0', axis = 1)

df_test = df_test[['test.csv', 'C1', 'C2', 'C3', 'C4', 'C5', 'C7', 'C8', 'C10', 'l1', 'l2', 'C12']]

# setting x,y
#X_df_test = df_test.iloc[:, 0:].values


# scaling the data
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
df_test = sc.fit_transform(df_test)

df_pred = model_1.predict(df_test)
