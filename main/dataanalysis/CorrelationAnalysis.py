import random, re, csv
import numpy as np
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from simdata import *
from interdata_mysql_simple import *

#/Users/cancui/anaconda3/envs/abiba_analysis_v2/src/main/resources/ilpddata/


mixdata_sim_filedir='../resources/gamedata/mixdata_sim.csv'
mixdata_sim=get_mldata(mixdata_sim_filedir)
print(mixdata_sim[0])



'''
mldata=simdata.get_features_labels(mixdata,14,0.4)

train_features=mldata['train_features']
test_features=mldata['test_features']

X = np.array(train_features)
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
kresult=kmeans.predict(test_features)

'''








