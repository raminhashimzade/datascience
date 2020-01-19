#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 12:39:44 2020

@author: ramin
"""


"""

https://data.world/search?context=community&q=Chronic+Disease&type=all

id      number
agein   days
gender  1 - women, 2 - men
height  cm
weight  kg
ap_hiSystolic     blood pressure
ap_loDiastolic    blood pressure
cholesterol       1: normal, 2: above normal, 3: well above normal
gluc              1: normal, 2: above normal, 3: well above normal
smoke             whether patient smokes or not
alco              Binary feature
active            Binary feature
cardio            Target variable

"""


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

df = pd.read_csv("/home/ramin/git/guru/model-cardio-disease/data.csv")
df.age_year = df.age_year.round()
df.drop("id", axis=1, inplace = True)
df.drop("age_days", axis=1, inplace = True)

X = df.iloc[:, :11]
y = df.iloc[:, 11]


# correlationgeldim
corrMatrix = df.corr()
sns.heatmap(corrMatrix, annot=True, linewidths=10)
sns.countplot(x="cardio", data=df, hue ='gender').set_title("GENDER - Heart Diseases")


# boxplot
df.boxplot()
plt.boxplot(df[(df['cardio']==1) & (df["gender"]==2)].weight)
plt.boxplot(df[(df['cardio']==1) & (df["gender"]==1)].weight)


# split data 
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=4)
print ('Train set:', X_train.shape,  y_train.shape)
print ('Test set:', X_test.shape,  y_test.shape)






"""
######################### KNeighborsClassifier = 64%
from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier(n_neighbors=2).fit(X_train,y_train)
y_pred = model.predict(X_test)

### Making the Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print("KNeighborsClassifier")
print(cm)
print('Accurancy: {:.0f}%'.format(model.score(X_test, y_test)*100))
"""


######################### DecisionTree = 73%
from sklearn.tree import DecisionTreeClassifier
model_tree = DecisionTreeClassifier(criterion="entropy", max_depth = 10)
model_tree.fit(X_train, y_train)
y_pred = model_tree.predict(X_test)

### Making the Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print("DecisionTree")
print(cm)
print('Accurancy: {:.0f}%'.format(model_tree.score(X_test, y_test)*100))



"""
######################### Naive Bayes = 59%
from sklearn.naive_bayes import BaseDiscreteNB
classifier = BaseDiscreteNB()
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

### Making the Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print("DecisionTree")
print(cm)
print('Accurancy: {:.0f}%'.format(classifier.score(X_test, y_test)*100))
"""





import matplotlib.pyplot as plt

cardio_1 = plt.scatter('age_year', 'cholesterol', data=df[(df['cardio']==0) & (df['gender']==2)], marker='o', color='green')
cardio_2 = plt.scatter('age_year', 'cholesterol', data=df[(df['cardio']==1) & (df['gender']==2)], marker='o', color='red')


sns.barplot(x=df.age_year,y=df.smoke.index)





sns.catplot(x="age_year", y="cardio", data=df);


sns.countplot(y="weight", hue="cardio", data=df)


sns.countplot(x="gender", data=df)
sns.countplot(x="cardio", data=df)
sns.countplot(x="gender", hue="cardio", data=df)


sns.countplot(x="smoke", hue=["cardio","gender"], data=df)


sns.pairplot(df)


des = df.describe()



import matplotlib.pyplot as plt
fig = plt.figure()

cardio_0 = plt.scatter('age_year', 'weight', data=df[(df['smoke']==0) & (df['cardio']==0)], marker='o', color='green')
cardio_1 = plt.scatter('age_year', 'weight', data=df[(df['smoke']==1) & (df['cardio']==0)], marker='o', color='Orange')
cardio_1 = plt.scatter('age_year', 'weight', data=df[(df['smoke']==1) & (df['cardio']==1)], marker='o', color='red')
cardio_1 = plt.scatter('age_year', 'weight', data=df[(df['smoke']==0) & (df['cardio']==1)], marker='o', color='blue')

cardio_0 = plt.scatter('age_year', 'weight', data=df[df['smoke']==0 & df['cardio']==0], marker='o', color='green')
cardio_1 = plt.scatter('age_year', 'weight', data=df[df['cardio']==1], marker='o', color='red')




























fig, ax = plt.subplots(figsize=(50,50))