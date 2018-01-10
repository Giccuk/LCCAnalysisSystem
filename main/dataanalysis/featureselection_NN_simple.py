from sklearn import datasets, svm, linear_model
from sklearn.model_selection import train_test_split
import tensorflow as tf
import numpy as np
import simdata

#========================
# DATA
#========================
seedsdatafiledir='../resources/seeds/seeds_dataset.txt'
seedsdata=simdata.get_seedsdata(seedsdatafiledir)

data_features=[]
data_labels=[]
for i in seedsdata:
	data_features=data_features+[i[0:7]]
	if i[7] ==1:
		data_labels=data_labels+[[1,0,0]]
	elif i[7]==2:
		data_labels=data_labels+[[0, 1, 0]]
	else:
		data_labels=data_labels+[[0,0,1]]


X = np.array(data_features)
Y = np.array(data_labels)


train_features, test_features, train_labels, test_labels = train_test_split(X, Y, test_size=0.33)



#==========================
# Set Network Structure
#==========================
#variables for network
num_features=7
num_hidden_units_layer1=4
num_output_units=3

#input/output information
NN_input=tf.placeholder(tf.float32,[None, num_features],name="NN_input")
NN_output=tf.placeholder(tf.float32,[None, num_output_units],name="NN_output")


#hidden layer1
weight1=tf.get_variable('w1',[num_features,num_hidden_units_layer1],tf.float32)
biase1=tf.get_variable('b1',[num_hidden_units_layer1],tf.float32)
l1_output=tf.sigmoid(tf.matmul(NN_input,weight1)+biase1)

#output layer
weight2=tf.get_variable('w2',[num_hidden_units_layer1,num_output_units],tf.float32)
biase2=tf.get_variable('b2',[num_output_units],tf.float32)
output_logits=tf.matmul(l1_output,weight2)+biase2

#train methods
## loss function
#loss=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=NN_output,logits=output_logits))
loss = tf.nn.l2_loss(output_logits - NN_output)

l1_regularizer=tf.contrib.layers.l1_regularizer(scale=0.1,scope=None)
loss_fun=loss+tf.contrib.layers.apply_regularization(l1_regularizer,[weight1])
## train method
train_step = tf.train.AdamOptimizer(0.005).minimize(loss_fun)
#train_step=tf.train.GradientDescentOptimizer(0.005).minimize(loss_fun)


#===========================
# Train Network
#===========================
sess=tf.InteractiveSession()
tf.global_variables_initializer().run()

for i in range(50000):
	batch_xs,batch_ys=(train_features,train_labels)
	sess.run(train_step,feed_dict={NN_input:batch_xs,NN_output:batch_ys})

#=============================
# Evaluation
#=============================
#test trained model
correct_prediction=tf.equal(tf.argmax(NN_output,1),tf.argmax(output_logits,1))
prediction_accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

train_accuracy=sess.run(prediction_accuracy,feed_dict={NN_input:train_features,NN_output:train_labels})
test_accuracy=sess.run(prediction_accuracy,feed_dict={NN_input:test_features,NN_output:test_labels})

print(train_accuracy)
print(test_accuracy)

#===================
# Show variable
#===================
w1=sess.run(weight1)
weight1_sum=np.sum(w1,axis=1)
min_feature=np.argmin(np.abs(weight1_sum))




