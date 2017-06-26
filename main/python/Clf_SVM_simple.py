import MLData,random
import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score

#MLData.build_interactiondataset()
svm_data=MLData.get_ilpddata()
#svm_data=MLData.get_interactiondata_sim()
train_labels=svm_data['train_labels']
train_features=svm_data['train_features']
test_labels=svm_data['test_labels']
test_features=svm_data['test_features']

svmclf=svm.SVC()
svmclf.fit(train_features,train_labels)
svmclfresult=svmclf.predict(test_features)

print accuracy_score(test_labels,svmclfresult)