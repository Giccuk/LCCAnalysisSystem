from sklearn import datasets, svm, linear_model
import tensorflow as tf
import numpy as np
import MLData

#========================
# DATA
#========================
seedsdatafiledir='/Users/cancui/workspace/virENV/lccanalysissystem/src/main/resources/seeds/seeds_dataset.txt'
seedsdata=MLData.get_seedsdata(seedsdatafiledir)

train_labels=np.array(seedsdata['train_labels_mat'])
train_features=np.array(seedsdata['train_features'])
test_labels=np.array(seedsdata['test_labels_mat'])
test_features=np.array(seedsdata['test_features'])

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
cross_entropy=tf.reduce_mean(
	tf.nn.softmax_cross_entropy_with_logits(labels=NN_output,logits=output_logits))
l1_regularizer=tf.contrib.layers.l1_regularizer(scale=0.1,scope=None)
loss_fun=cross_entropy+tf.contrib.layers.apply_regularization(l1_regularizer,[weight1])
## train method
train_step=tf.train.GradientDescentOptimizer(0.05).minimize(loss_fun)


#===========================
# Train Network
#===========================
sess=tf.InteractiveSession()
tf.global_variables_initializer().run()
for i in range(1000):
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

#===================
# Show variable
#===================
w1=sess.run(weight1)
weight1_sum=np.sum(w1,axis=1)
min_feature=np.argmin(np.abs(weight1_sum))


print test_accuracy
print min_feature




