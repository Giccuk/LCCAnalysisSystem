import random,re,csv
import numpy as np
import GameDataMySQL
#=============================================
#ILPD (Indian Liver Patient Dataset) Data Set
#=============================================
def get_ilpddata():
	ilpddata = np.genfromtxt(
		'/Users/cancui/workspace/virENV/lccanalysissystem/src/main/resources/ilpd/ilpddata2.csv',
		delimiter=',')
	dataset_shape=ilpddata.shape
	label_indx=dataset_shape[1]-1
	train_sample_num=int(round(dataset_shape[0]*0.6))
	train_features=ilpddata[0:train_sample_num,0:label_indx]
	train_labels=ilpddata[0:train_sample_num,label_indx]
	test_features = ilpddata[train_sample_num:dataset_shape[0], 0:label_indx]
	test_labels = ilpddata[train_sample_num:dataset_shape[0], label_indx]
	#delete rows contain nan variables in train data sets
	nan_line_indx=[]
	for i in range(0,train_features.shape[0]):
		for j in train_features[i,:]:
			if np.isnan(j):
				nan_line_indx=nan_line_indx+[i]
	if nan_line_indx:
		train_features=np.delete(train_features,[nan_line_indx],0)
		train_labels=np.delete(train_labels,[nan_line_indx],0)
	# delete rows contain nan variables in test data sets
	nan_line_indx = []
	for i in range(0,test_features.shape[0]):
		for j in test_features[i,:]:
			if np.isnan(j):
				nan_line_indx=nan_line_indx+[i]
	if nan_line_indx:
		test_features=np.delete(train_features,[nan_line_indx],0)
		test_labels=np.delete(train_labels,[nan_line_indx],0)
	return {'train_features':train_features,
			'train_labels':train_labels,
			'test_features':test_features,
			'test_labels':test_labels}

#=======================
# seeds data
#=======================
#read data from file
def get_seedsdata():
	datasrc="/Users/cancui/workspace/virENV/lccanalysissystem/src/main/resources/seeds/seeds_dataset.txt"
	with open(datasrc,"r") as seedssrcfile:
		  seedssrclines=seedssrcfile.readlines()

	#divide strings by ","
	seedssrcdata=[]
	for eachline in seedssrclines:
		rresult=eachline.replace("\t",",")
		seedssrcdata=seedssrcdata+[rresult]

	#abstrace features and labels
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

	#build test and train sets
	trainpos=range(0,31)+range(101,136)+range(181,210)
	testpos=range(31,101)+range(136,181)
	train_features=[]
	train_labels=[]
	test_features=[]
	test_labels=[]
	for i in trainpos:
		train_features=train_features+[seedsdata[i][0:7]]
		train_labels=train_labels+[seedsdata[i][7]]
	for i in testpos:
		test_features=test_features+[seedsdata[i][0:7]]
		test_labels=test_labels+[seedsdata[i][7]]

	train_labels_mat=[]
	test_labels_mat=[]
	for i in range(len(train_labels)):
		if train_labels[i]==1:
			train_labels_mat=train_labels_mat+[[1,0,0]]
		elif train_labels[i]==2:
			train_labels_mat=train_labels_mat+[[0,1,0]]
		elif train_labels[i]==3:
			train_labels_mat=train_labels_mat+[[0,0,1]]
	for i in range(len(test_labels)):
		if test_labels[i] == 1:
				test_labels_mat = test_labels_mat + [[1, 0, 0]]
		elif test_labels[i] == 2:
				test_labels_mat = test_labels_mat + [[0, 1, 0]]
		elif test_labels[i] == 3:
				test_labels_mat = test_labels_mat + [[0, 0, 1]]

	return {'train_features':train_features,
			'train_labels':train_labels,
			'train_labels_mat':train_labels_mat,
			'test_features':test_features,
			'test_labels':test_labels,
			'test_labels_mat':test_labels_mat}

#=================
#game data
#=================
def get_interactiondata_MySQL(dbaddress):
	gamemessages=GameDataMySQL.getgamedataMySQL(dbaddress)
	offerratio=GameDataMySQL.getofferratio(gamemessages)
	acceptornotratio=GameDataMySQL.getacceptornotratio(gamemessages)
	investratio=GameDataMySQL.getinvestratio(gamemessages)
	repayratio=GameDataMySQL.getrepayratio(gamemessages)
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
	return {'features':samples,'labels':labels}

#==========================
#simulated interaction data
#1. OR:offer_rate, AR:accept_rate, IR:invest_rate, RR:repay_rate
#2. depressive: OR:[0.6,0,9], AR:[0.4,1.0], IR:[0.5,0.7], RR:[0.4,0.6]
#   no_depessive: OR:[0.3,0.5], AR:[0.6,1.0], IR:[0.1,0.3], RR:[0.1,0.3]
#3. "1" for depression, "0" for not_depression
#==========================
def build_interactiondataset():
	behavior_data=[]
	for i in range(1,10000):
		dep_offerrate = random.choice(range(6, 10))
		dep_acceptrate = random.choice(range(4, 10))
		dep_investrate = random.choice(range(5, 8))
		dep_repayrate = random.choice(range(4, 6))
		notdep_offerrate = random.choice(range(3, 6))
		notdep_acceptrate = random.choice(range(6, 10))
		notdep_investrate = random.choice(range(1, 4))
		notdep_repayrate = random.choice(range(1, 4))
		behavior_data=behavior_data+[[dep_offerrate,dep_acceptrate,dep_investrate, dep_repayrate,1]]
		behavior_data=behavior_data+[[notdep_offerrate,notdep_acceptrate,notdep_investrate,notdep_repayrate,0]]
	random.shuffle(behavior_data)
	with open('/Users/cancui/workspace/virENV/lccanalysissystem/src/main/resources/behaviordata/behaviordata.csv','wb') as datafile:
		datawriter=csv.writer(datafile)
		for line in behavior_data:
			datawriter.writerow(line)

def get_interactiondata_sim():
		behaviordata=np.genfromtxt('/Users/cancui/workspace/virENV/lccanalysissystem/src/main/resources/behaviordata/behaviordata.csv',delimiter=',')
		data_shape=behaviordata.shape
		sample_num=data_shape[0]
		feature_num=data_shape[1]-1
		train_sample_num=int(round(sample_num*0.6))
		train_features=behaviordata[0:train_sample_num,0:feature_num]
		train_labels=behaviordata[0:train_sample_num,feature_num]
		test_features=behaviordata[train_sample_num:sample_num,0:feature_num]
		test_labels=behaviordata[train_sample_num:sample_num,feature_num]
		return{'train_features':train_features,
			   'train_labels':train_labels,
			   'test_features':test_features,
			   'test_labels':test_labels}


