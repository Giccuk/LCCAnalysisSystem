from sklearn.cluster import KMeans
import numpy as np
import MLData
from scipy import stats
from sklearn.metrics import accuracy_score
from sklearn import metrics

interdatafiledir_sim='/Users/cancui/workspace/virENV/lccanalysissystem/src/main/resources/behaviordata_sim/behaviordata_sim.csv'
kmdata=MLData.get_interactiondata_sim(interdatafiledir_sim)

#iplddatafiledir='/Users/cancui/workspace/virENV/lccanalysissystem/src/main/resources/ilpddata/ilpddata2.csv'
#svm_data=MLData.get_ilpddata(iplddatafiledir)

train_labels=kmdata['train_labels']
train_features=kmdata['train_features']
test_labels=kmdata['test_labels']
test_features=kmdata['test_features']

#========================
# kmeans
#========================
def addone(x): return x+1
X = np.array(train_features)
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
kresult=kmeans.predict(test_features)
'''
for i in range(len(kresult)):
	if kresult[i]==0:
		kresult[i]=1
	else:
		kresult[i]=0
'''

print kresult
print test_labels
print stats.ttest_ind(kresult,test_labels)
print accuracy_score(kresult,test_labels)

print metrics.adjusted_rand_score(kresult,test_labels)