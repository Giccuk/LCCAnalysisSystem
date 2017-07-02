from sklearn.cluster import KMeans

import numpy as np
import MLData

svm_data=MLData.get_interactiondata_sim()
train_labels=svm_data['train_labels']
train_features=svm_data['train_features']
test_labels=svm_data['test_labels']
test_features=svm_data['test_features']
#========================
# kmeans
#========================
def addone(x): return x+1
X = np.array(train_features)
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
kresult=kmeans.predict(test_features)
for i in range(len(kresult)):
	if kresult[i]==0:
		kresult[i]=1
	else:
		kresult[i]=0

dis=0
for i in range(len(kresult)):
	if kresult[i]!=test_labels[i]:
		print (kresult[i],test_labels[i])
		dis+=1

print dis