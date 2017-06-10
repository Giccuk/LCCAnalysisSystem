import tensorflow as tf
import random,re
import numpy as np

num_features = 7
num_hidden_units_layer1 = 4
num_output_units = 3

#===========
#data
#============
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

trainlabelmat=[]
testlabelmat=[]

for i in range(len(trainlabels)):
    if trainlabels[i]==1:
        trainlabelmat=trainlabelmat+[[1,0,0]]
    elif trainlabels[i]==2:
        trainlabelmat=trainlabelmat+[[0,1,0]]
    elif trainlabels[i]==3:
        trainlabelmat=trainlabelmat+[[0,0,1]]

for i in range(len(testlabels)):
    if testlabels[i] == 1:
            testlabelmat = testlabelmat + [[1, 0, 0]]
    elif testlabels[i] == 2:
            testlabelmat = testlabelmat + [[0, 1, 0]]
    elif testlabels[i] == 3:
            testlabelmat = testlabelmat + [[0, 0, 1]]


inputy=np.array(trainlabelmat)
inputx=np.array(trainfeatures)
testy=np.array(testlabelmat)
testx=np.array(testfeatures)

#exit()


#===========
# nn
#==========
X = tf.placeholder(tf.float32, [None, num_features], name="inputs")
Y = tf.placeholder(tf.float32, [None, num_output_units], name="outputs")

#hidden layer1
W1 = tf.get_variable("w1", [num_features, num_hidden_units_layer1], tf.float32)
b1 = tf.get_variable("b1", [num_hidden_units_layer1], tf.float32)
l1_output = tf.sigmoid(tf.matmul(X, W1) + b1)

#output layer
W2 = tf.get_variable("w2", [num_hidden_units_layer1, num_output_units], tf.float32)
b2 = tf.get_variable("b2", [num_output_units], tf.float32)
output_logits = tf.matmul(l1_output, W2) + b2

cross_entropy = tf.reduce_mean(
      tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=output_logits))

l1_regularizer = tf.contrib.layers.l1_regularizer(scale=0.1, scope=None)

loss = cross_entropy + tf.contrib.layers.apply_regularization(l1_regularizer, [W1])
train_step = tf.train.GradientDescentOptimizer(0.05).minimize(loss)

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

# Train
for i in range(50000):
    #print str(i) + "/3000"
    batch_xs, batch_ys = (inputx, inputy)
    sess.run(train_step, feed_dict={X: batch_xs, Y: batch_ys})

# Test trained model
correct_prediction = tf.equal(tf.argmax(Y, 1), tf.argmax(output_logits, 1))

accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

print(sess.run(accuracy, feed_dict={X: inputx,Y: inputy}))
print(sess.run(accuracy, feed_dict={X: testx,Y: testy}))

w1 = sess.run(W1)

w1_sum = np.sum(w1, axis=1)
min_feature = np.argmin(np.abs(w1_sum))

print w1
print "_____________"
print w1_sum
print min_feature