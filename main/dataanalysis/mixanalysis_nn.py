import tensorflow as tf
import numpy as np
from simdata import get_mldata
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
######################################
# Getting data from data sources
######################################
#=========================
#get data from csv files
#=========================
mixdata_sim_filedir='../resources/gamedata/mixdata_sim.csv'
inerdata_sim_filedir='../resources/gamedata/interdata_sim.csv'
biodata_sim_filedir='../resources/gamedata/biodata_sim.csv'

mixdata_sim=get_mldata(mixdata_sim_filedir)
interdata_sim=get_mldata(inerdata_sim_filedir)
biodata_sim=get_mldata(biodata_sim_filedir)

'''
#===================================
# make data for analysis
#===================================
interdata_sim_features=[]
biodata_sim_features=[]
for i in interdata_sim:
    interdata_sim_features=interdata_sim_features+[i[0:4]]
for i in biodata_sim:
    biodata_sim_features=biodata_sim_features+[i[0:10]]
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
labels_nn=[]
for i in labels_pre_km:
    if i==0:
        #labels_nn=labels_nn+[labels_pre_km_centers[0]]
        labels_nn=labels_nn+[[0.]]
    else:
        #labels_nn=labels_nn+[labels_pre_km_centers[1]]
        labels_nn=labels_nn+[[1.]]

labels_nn_np = np.array(labels_nn)

features_nn=[]
for i in mixdata_sim:
    features_nn=features_nn+[i[4:14]]

features_nn_np = np.array(features_nn)
features_nn_np = (features_nn_np - features_nn_np.mean(axis=0)) / features_nn_np.std(axis=0)# data scaling

train_features, test_features, train_labels, test_labels = train_test_split(features_nn_np, labels_nn_np, test_size=0.33)


#==========================
# Set Network Structure
#==========================
#variables for network
num_features=10
num_hidden_units_layer1=200
num_hidden_units_layer2=200
num_hidden_units_layer3=200
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

#comparepair=[NN_output,output_logits]
#correct_accuracy=tf.reduce_mean(comparepair,)

c_pred_acc = sess.run(prediction_accuracy,feed_dict={NN_input:test_features, NN_output: test_labels})
c_pred_acc_train = sess.run(prediction_accuracy, feed_dict={NN_input: train_features, NN_output: train_labels})

print("test acc: ", c_pred_acc)
print("training acc: ", c_pred_acc_train)






