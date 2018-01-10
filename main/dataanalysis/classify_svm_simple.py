import simdata,random
import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score


#interdatafiledir_sim='/Users/cancui/workspace/virENV/lccanalysissystem/src/main/resources/behaviordata_sim/behaviordata_sim.csv'
#simdata.build_interactiondata(interdatafiledir_sim)
#new_data=simdata.get_interactiondata_sim(interdatafiledir_sim)

ilpdatafiledir='/Users/cancui/workspace/virENV/lccanalysissystem/src/main/resources/ilpddata/ilpddata2.csv'
svm_data=simdata.get_ilpddata(ilpdatafiledir)

train_labels=svm_data['train_labels']
train_features=svm_data['train_features']
test_labels=svm_data['test_labels']
test_features=svm_data['test_features']

svmclf=svm.SVC(C=1)
svmclf.fit(train_features,train_labels)
svmclfresult=svmclf.predict(test_features)

scores=cross_val_score(svmclf,train_features,train_labels,cv=4)

print scores
print accuracy_score(test_labels,svmclfresult)
print test_labels.shape,train_labels.shape