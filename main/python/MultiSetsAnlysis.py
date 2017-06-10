import QueryGameSeq
import GameDataMySQL
from sklearn import datasets, svm, linear_model
from sklearn.cluster import KMeans
import random,re
import numpy as np
from numpy import array

#=================
#game data
#=================
gamemessages=GameDataMySQL.getinterseqMySQL("localhost")
offerratio=QueryGameSeq.getofferratio(gamemessages)
acceptornotratio=QueryGameSeq.getacceptornotratio(gamemessages)
investratio=QueryGameSeq.getinvestratio(gamemessages)
repayratio=QueryGameSeq.getrepayratio(gamemessages)
samples=[]
labels=[]
for i in range(len(offerratio)):
	if i<len(acceptornotratio[0]):
		#print [offerratio[i],acceptornotratio[0][i]]
		samples=samples+[[offerratio[i],acceptornotratio[0][i]]]
	else:
		j=i-len(acceptornotratio[0])
		#print [offerratio[i],acceptornotratio[1][j]]
		samples=samples+[[offerratio[i],acceptornotratio[1][j]]]
	label_rand=random.randint(0,2)
	labels=labels+[label_rand]

#==========================
#seeds data
#==========================
datasrc="/Users/cancui/workspace/virENV/lccanalysissystem/src/main/resources/seeds/seeds_dataset.txt"
with open(datasrc,"r") as seedssrcfile:
	  seedssrclines=seedssrcfile.readlines()
seedssrcdata=[]

for eachline in seedssrclines:
	rresult=eachline.replace("\t",",")
	seedssrcdata=seedssrcdata+[rresult]

seedsdata=[]
pattern_feature=re.compile(r'(\d+\.*\d*),')
pattern_label=re.compile(r',(\d)\n')
for linei in range(len(seedssrcdata)):
	if linei<(len(seedssrcdata)-1):
		featureresult=re.findall(pattern_feature,seedssrcdata[linei])
		labelresult=re.findall(pattern_label,seedssrcdata[linei])
		seedsdata=seedsdata+[map(float,featureresult)+map(float,labelresult)]
	else:
		featureresult=re.findall(pattern_feature,seedssrcdata[linei])
		lenlastline=len(seedssrcdata[linei])
		pos=lenlastline-1
		seedsdata=seedsdata+[map(float,featureresult)+[float(seedssrcdata[linei][pos])]]

trainpos=range(0,31)+range(101,136)+range(181,210)
testpos=range(31,101)+range(136,181)
trainfeatures=[]
trainlabels=[]
testfeatures=[]
testlabels=[]
for i in trainpos:
	trainfeatures=trainfeatures+[seedsdata[i][0:7]]
	trainlabels=trainlabels+[seedsdata[i][7]]
for i in testpos:
	testfeatures=testfeatures+[seedsdata[i][0:7]]
	testlabels=testlabels+[seedsdata[i][7]]


#=======================
# svm
#=======================
svmclf=svm.SVC()
svmclf.fit(trainfeatures,trainlabels)
svmclfresult=svmclf.predict(testfeatures)
svmclf_dis=[]
for i in range(len(testfeatures)):
	dis=float(svmclfresult[i])-testlabels[i]
	svmclf_dis=svmclf_dis+[dis]
svmclf_dismean=np.mean(map(abs,svmclf_dis))
svmclf_disvar=np.var(svmclf_dis)
print "svmclf_dismean is %d" %svmclf_dismean
print "svmclf_disvar is %d" %svmclf_disvar
#========================
# kmeans
#========================
def addone(x): return x+1
X = np.array(trainfeatures)
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

kresult=kmeans.predict(testfeatures)
kresult_addone=map(addone,kresult)
dis=0
for i in range(len(kresult_addone)):
	if kresult_addone[i]!=testlabels[i]:
		dis+=1

#================
#regression
#================
#basic----------------------------------------
'''
basicreg = linear_model.LinearRegression()
basicreg.fit (trainfeatures,trainlabels)
coefresult=basicreg.coef_
basicreg_dis=[]
for i in range(len(trainlabels)):
	predictlabel=np.dot(trainfeatures[i],coefresult)
	dis=predictlabel-trainlabels[i]
	basicreg_dis=basicreg_dis+[dis]
basicreg_dismean=np.mean(map(abs,basicreg_dis))
basicreg_disvar=np.var(basicreg_dis)
'''
#lasso--------------------------------------
lassoreg = linear_model.Lasso(alpha = 0.1)
lassoreg.fit(trainfeatures,trainlabels)
coefresult=lassoreg.coef_
lassoreg_dis=[]
for i in range(len(trainlabels)):
	predictlabel=np.dot(trainfeatures[i],coefresult)
	dis=predictlabel-trainlabels[i]
	lassoreg_dis=lassoreg_dis+[dis]
a=map(abs,lassoreg_dis)
lassoreg_dismean=np.mean(a)
lassoreg_disvar=np.var(lassoreg_dis)
print coefresult
