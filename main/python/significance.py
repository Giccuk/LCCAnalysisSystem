#=====================
#significance test
#=====================
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

a=[[0,1]]
b=[0]
for i in range(1,10):
    a=a+[[i*2,i*2+1]]
    b=b+[i%2]

print a,b

train_features,test_features,train_labels,test_labels=train_test_split(
    a,b,test_size=0.4,random_state=0
)

print train_features,train_labels
print stats.ttest_ind(a,b)
