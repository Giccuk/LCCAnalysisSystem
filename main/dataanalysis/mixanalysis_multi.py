import tensorflow as tf
from sklearn import svm
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
'''
mixdata_sim=[]
for i in range(len(interdata_sim)):
    mixdata_sim=mixdata_sim+[biodata_sim[i][0:10]+biodata_sim[i]]
print(mixdata_sim[0])
'''



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
cluster_inter=KMeans(n_clusters=2,random_state=0).fit(features_km_np)


#============================
#labels from cluster
#============================
labels_pre_clu=cluster_inter.labels_
labels_pre_clu_centers=cluster_inter.cluster_centers_

#######################################
# Classify samples
#######################################
#================================
# data for classifying analysis
#================================
labels_cla=[]
for i in labels_pre_clu:
    if i==0:
        #labels_cla=labels_cla+[labels_pre_clu_centers[0]]
        labels_cla=labels_cla+[[0.]]
    else:
        #labels_cla=labels_cla+[labels_pre_clu_centers[1]]
        labels_cla=labels_cla+[[1.]]

labels_cla_np = np.array(labels_cla)

features_cla=[]
for i in mixdata_sim:
    features_cla=features_cla+[i[4:14]]

features_cla_np = np.array(features_cla)
features_cla_np = (features_cla_np - features_cla_np.mean(axis=0))/features_cla_np.std(axis=0)# follow natural distribution

train_features, test_features, train_labels, test_labels = train_test_split(features_cla_np, labels_cla_np, test_size=0.33)

#============================
#classify biodata by SVM
#============================
clf_svm=svm.SVC(C=1)
clf_svm.fit(train_features,train_labels)
labels_pre_svm=clf_svm.predict(test_features)

#===============================
#classify biodata by GaussianNB
#===============================
clf_gnb=GaussianNB()
clf_gnb.fit(train_features,train_labels)
labels_pre_gnb=clf_gnb.predict(test_features)

#====================================
#classify biodata by Neural Network
#====================================
#==========================
# Set Network Structure
#==========================
#variables for network
num_features=10
num_hidden_units_layer1=100
num_hidden_units_layer2=100
num_hidden_units_layer3=100
num_output_units=1

#input/output information
NN_input=tf.placeholder(tf.float32,[None, num_features],name="NN_input")
NN_output=tf.placeholder(tf.float32,[None, num_output_units],name="NN_output")


#hidden layer1
weight1=tf.get_variable('w1',[num_features,num_hidden_units_layer1],tf.float32)
biase1=tf.get_variable('b1',[num_hidden_units_layer1],tf.float32)
#l1_output=tf.sigmoid(tf.matmul(NN_input,weight1)+biase1)
l1_output = tf.nn.relu(tf.matmul(NN_input, weight1)+biase1)

#hidden layer2
weight2=tf.get_variable('w2',[num_features,num_hidden_units_layer2],tf.float32)
biase2=tf.get_variable('b2',[num_hidden_units_layer2],tf.float32)
#l2_output=tf.sigmoid(tf.matmul(NN_input,weight1)+biase1)
l2_output = tf.nn.relu(tf.matmul(NN_input, weight2)+biase2)

#hidden layer2
weight3=tf.get_variable('w3',[num_features,num_hidden_units_layer3],tf.float32)
biase3=tf.get_variable('b3',[num_hidden_units_layer3],tf.float32)
#l3_output=tf.sigmoid(tf.matmul(NN_input,weight1)+biase1)
l3_output = tf.nn.relu(tf.matmul(NN_input, weight3)+biase3)

#output layer
weight_out=tf.get_variable('w_out',[num_hidden_units_layer3,num_output_units],tf.float32)
biase_out=tf.get_variable('b_out',[num_output_units],tf.float32)

output_logits=tf.matmul(l3_output,weight_out)+biase_out
output = tf.nn.sigmoid(output_logits)

#train methods
#loss=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=NN_output,logits=output_logits)) #to be used for [[0,1,0],[1,0,0]...[]]
#loss = tf.nn.l2_loss(output_logits - NN_output)
loss = tf.nn.sigmoid_cross_entropy_with_logits(logits=output_logits, labels=NN_output)

l1_regularizer=tf.contrib.layers.l1_regularizer(scale=0.1,scope=None)
loss_fun=loss+tf.contrib.layers.apply_regularization(l1_regularizer,[weight3])

# train method
train_step = tf.train.AdamOptimizer(0.0001).minimize(loss_fun)
#train_step=tf.train.GradientDescentOptimizer(0.005).minimize(loss_fun)


#===========================
# Train Network
#===========================
sess=tf.InteractiveSession()
tf.global_variables_initializer().run()
#init_g=tf.global_variables_initializer()
#init_l=tf.local_variables_initializer()

for i in range(20000):
    batch_xs,batch_ys=(train_features,train_labels)
    c_loss, _ = sess.run([loss, train_step],feed_dict={NN_input:batch_xs,NN_output:batch_ys})
    #print(c_loss)

#=============================
# Evaluation
#=============================

correct_prediction = tf.equal(tf.round(NN_output), tf.round(output))
prediction_accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
acc_nn = sess.run(prediction_accuracy,feed_dict={NN_input:test_features, NN_output: test_labels})
print("acc_nn:",acc_nn)

acc_gnb=accuracy_score(test_labels,labels_pre_gnb)
print("acc_gnb:",acc_gnb)

acc_svm=accuracy_score(test_labels,labels_pre_svm)
print("acc_svm:",acc_svm)

acc_dic={'classifier_name':["nn","svm","gnb"],'classifier_acc':[acc_nn,acc_svm,acc_gnb]}
highest_acc_index=np.argmax(acc_dic)
print("the best classifier is:",acc_dic["classifier_name"][highest_acc_index])
#=================
# analysis
#=================
biolabels=[]
interlabels=[]
for i in range(len(biodata_sim)):
    biolabels=biolabels+[biodata_sim[i][10]]

biolabels_np=np.array(biolabels)

cluster_labels=[]
classify_labels=labels_pre_svm
for i in range(len(labels_pre_clu)):
    if labels_pre_clu[i]==1:
        cluster_labels=cluster_labels+[0]
    else:
        cluster_labels = cluster_labels + [1]

acc_clu_bio=accuracy_score(biolabels,cluster_labels)
print("acc_clu_bio:",acc_clu_bio)



