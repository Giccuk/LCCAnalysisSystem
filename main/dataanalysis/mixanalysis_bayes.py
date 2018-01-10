from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
import numpy as np
from simdata import get_mldata
from sklearn.model_selection import train_test_split
######################################
# Getting data from data sources
######################################
#=========================
#get data from csv files
#=========================
mixdata_sim_filedir='../resources/gamedata/mixdata_sim.csv'
mixdata_sim=get_mldata(mixdata_sim_filedir)


inerdata_sim_filedir='../resources/gamedata/interdata_sim.csv'
biodata_sim_filedir='../resources/gamedata/biodata_sim.csv'
interdata_sim=get_mldata(inerdata_sim_filedir)
biodata_sim=get_mldata(biodata_sim_filedir)

############################################
# Clustering based on interdata
############################################
#===========================
# get data for clustering
#===========================
features_km=[]
for i in mixdata_sim:
    features_km=features_km+[i[0:4]]

features_km_np=np.array(features_km)
features_km_np = (features_km_np - features_km_np.mean(axis=0)) / features_km_np.std(axis=0)

#=================================
# cluster interdata by kmeans
#=================================

clu_km=KMeans(n_clusters=2,random_state=0).fit(features_km_np)
#labels_pre_km=kmeans.predict(features_interdata_sim[400:579])
#testlabels_true=label_interdata_sim[400:579]
#metrics.adjusted_rand_score(testlabels_true,testlabels_pre_km)

#============================
#labels for biodata
#============================
labels_pre_km=clu_km.labels_
labels_pre_km_centers=clu_km.cluster_centers_

#######################################
# Classify samples
#######################################
#================================
# data for classifying analysis
#================================
labels_svm=[]
for i in labels_pre_km:
    if i==0:
        #labels_svm=labels_svm+[labels_pre_km_centers[0]]
        labels_svm=labels_svm+[[0.]]
    else:
        #labels_svm=labels_svm+[labels_pre_km_centers[1]]
        labels_svm=labels_svm+[[1.]]

labels_svm_np = np.array(labels_svm)

features_svm=[]
for i in mixdata_sim:
    features_svm=features_svm+[i[4:14]]

features_svm_np = np.array(features_svm)
features_svm_np = (features_svm_np - features_svm_np.mean(axis=0))/features_svm_np.std(axis=0)# follow natural distribution


train_features, test_features, train_labels, test_labels = train_test_split(features_svm_np, labels_svm_np, test_size=0.33)

#============================
#classify biodata by GaussianNB
#============================
clf_gnb=GaussianNB()
clf_gnb.fit(train_features,train_labels)
labels_pre_gnb=clf_gnb.predict(test_features)


#============================
# Evaluation
#============================
acc_gnb=accuracy_score(test_labels,labels_pre_gnb)
print("acc_gnb:",acc_gnb)



#=================
# analysis
#=================
biolabels=[]
interlabels=[]
for i in range(len(biodata_sim)):
    biolabels=biolabels+[biodata_sim[i][10]]

biolabels_np=np.array(biolabels)

cluster_labels=[]
for i in range(len(labels_pre_km)):
    if labels_pre_km[i]==1:
        cluster_labels=cluster_labels+[0]
    else:
        cluster_labels = cluster_labels + [1]

acc_clu_bio=accuracy_score(biolabels,cluster_labels)
print("acc_clu_bio:",acc_clu_bio)



