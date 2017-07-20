import random, re, csv
import numpy as np
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
import MLData

datafiledir = '/Users/cancui/workspace/virENV/lccanalysissystem/src/main/resources/ilpddata/ilpddata2.csv'
ilpddata = MLData.get_ilpddata(datafiledir)
interdata = MLData.get_interdata_sim(ilpddata)
mixdata = MLData.get_mixdata(ilpddata, interdata)
mldata=MLData.get_featureslabel(mixdata,14,0.4)

print mldata['train_features'][0]
print mldata['train_features'][0][0:10]

train_features=mldata['train_features']
test_features=mldata['test_features']
X = np.array(train_features)
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
kresult=kmeans.predict(test_features)


cd 

#mixdata_ml=get_featureslabel(mixdata,13)





