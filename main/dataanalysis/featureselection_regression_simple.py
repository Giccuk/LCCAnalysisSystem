from sklearn.linear_model import LogisticRegression
from sklearn import linear_model
import numpy as np
import simdata
from sklearn.metrics import accuracy_score


#------------------------------
# Data
#------------------------------
interdata_sim_filedir='/Users/cancui/workspace/anaconda3/envs/abiba_analysis/src/main/resources/interdata_sim/interdata_sim.csv'
ilpddata_filedir='/Users/cancui/workspace/anaconda3/envs/abiba_analysis/src/main/resources/ilpddata/ilpddata2.csv'
inputdata=simdata.get_interdata_sim(interdata_sim_filedir)
inputdata=simdata.get_ilpddata(ilpddata_filedir)

train_labels_np=np.array(inputdata['train_labels'])
train_features_np=np.array(inputdata['train_features'])
test_labels_np=np.array(inputdata['test_labels'])
test_features_np=np.array(inputdata['test_features'])

#linear regression
reg_lasso_lin = linear_model.Lasso(alpha = 0.1)

#logistic regression
reg_logis=LogisticRegression(C=1,penalty='l1',tol=0.5)
reg_logis.fit(train_features_np,train_labels_np)
coefresult=reg_logis.coef_

predict_result=reg_logis.predict(test_features_np)
indx_mincoef=np.argmin(np.abs(coefresult))+1
predict_accuracy=accuracy_score(test_labels_np,predict_result)

print(train_features_np.shape)
print(coefresult)
print (indx_mincoef)
print (predict_accuracy)