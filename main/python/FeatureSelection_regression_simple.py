from sklearn.linear_model import LogisticRegression
from sklearn import linear_model
import numpy as np
import MLData
from sklearn.metrics import accuracy_score

inputdata=MLData.get_interactiondata_sim()
inputdata=MLData.get_ilpddata()

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

print train_features_np.shape
print coefresult
print indx_mincoef
print predict_accuracy