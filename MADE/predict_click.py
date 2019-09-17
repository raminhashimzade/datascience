#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 23:15:48 2019

@author: ramin
"""

import pandas as pd

df = pd.read_csv('train.tar.gz', compression='gzip', header=0, sep=';', quotechar='"', nrows=10000)

dfS = pd.read_csv('sample_submission.csv')



import seaborn as sns
sns.heatmap(df.corr(), annot=True)
corr = df.corr()

sns.countplot(y = 'CUS_CHILDS', data=dataset)