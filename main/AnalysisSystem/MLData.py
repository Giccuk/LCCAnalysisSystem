import random, re, csv
import numpy as np
from sklearn.model_selection import train_test_split


# =============================================
# ILPD (Indian Liver Patient Dataset) Data Set
# This data set contains
# 1. 416 liver patient records and 167 non liver patient records.
# 2. This data set contains 441 male patient records and 142 female patient records.
# Any patient whose age exceeded 89 is listed as being of age "90".
# 3. attribution information:
# 1) Age	Age of the patient
# 2) Gender	Gender of the patient (female:1, male:2)
# 3) TB	Total Bilirubin
# 4) DB	Direct Bilirubin
# 5) Alkphos Alkaline Phosphotase
# 6) Sgpt Alamine Aminotransferase
# 7) Sgot Aspartate Aminotransferase
# 8) TP	Total Protiens
# 9) ALB	Albumin
# 10) A/G Ratio	Albumin and Globulin Ratio
# 11) Selector field used to split the data into two sets (labeled by the expert
# =============================================
# '/Users/cancui/workspace/virENV/lccanalysissystem/src/main/resources/ilpddata/ilpddata2.csv',
def get_ilpddata(datafiledir):
    data = []
    with open(datafiledir, 'rb') as datafile:
        data_reader = csv.reader(datafile)
        for i in data_reader:
            flag = 0
            for j in i:
                if j == '':
                    flag = 1
            if flag == 0:
                okayline=[]
                for j in i:
                    okayline=okayline+[float(j)]
                data = data+[okayline]
    return data


'''
	ilpddata = np.genfromtxt(datafiledir, delimiter=',')
	dataset_shape=ilpddata.shape
	label_indx=dataset_shape[1]-1
	train_features,test_features,train_labels,test_labels=train_test_split(ilpddata[:,0:label_indx],ilpddata[:,label_indx],test_size=0.4,random_state=0)
	nan_line_indx=[]
	for i in range(0,train_features.shape[0]):
		for j in train_features[i,:]:
			if np.isnan(j):
				nan_line_indx=nan_line_indx+[i]
	if nan_line_indx:
		train_features=np.delete(train_features,[nan_line_indx],0)
		train_labels=np.delete(train_labels,[nan_line_indx],0)
	nan_line_indx=[]
	for i in range(0,test_features.shape[0]):
		for j in test_features[i,:]:
			if np.isnan(j):
				nan_line_indx=nan_line_indx+[i]
	if nan_line_indx:
		test_features=np.delete(test_features,[nan_line_indx],0)
		test_labels=np.delete(test_labels,[nan_line_indx],0)
	return {'train_features':train_features,
			'train_labels':train_labels,
			'test_features':test_features,
			'test_labels':test_labels}
'''


# =======================
# seeds data
# =======================
# read data from file
# "/Users/cancui/workspace/virENV/lccanalysissystem/src/main/resources/seeds/seeds_dataset.txt"
def get_seedsdata(datafiledir):
    with open(datafiledir, "r") as seedssrcfile:
        seedssrclines = seedssrcfile.readlines()
    # divide strings by ","
    seedssrcdata = []
    for eachline in seedssrclines:
        rresult = eachline.replace("\t", ",")
        seedssrcdata = seedssrcdata + [rresult]

    # abstrace features and labels
    seedsdata = []
    pattern_feature = re.compile(r'(\d+\.*\d*),')
    pattern_label = re.compile(r',(\d)\n')
    for linei in range(len(seedssrcdata)):
        if linei < (len(seedssrcdata) - 1):
            featureresult = re.findall(pattern_feature, seedssrcdata[linei])
            labelresult = re.findall(pattern_label, seedssrcdata[linei])
            seedsdata = seedsdata + [map(float, featureresult) + map(float, labelresult)]
        else:
            featureresult = re.findall(pattern_feature, seedssrcdata[linei])
            lenlastline = len(seedssrcdata[linei])
            pos = lenlastline - 1
            seedsdata = seedsdata + [map(float, featureresult) + [float(seedssrcdata[linei][pos])]]
    return seedsdata

# ==========================
# Get Simulated Interaction data
# 1. OR:offer_rate, AR:accept_rate, IR:invest_rate, RR:repay_rate
# 2. depressive: OR:[0.6,0,9], AR:[0.4,1.0], IR:[0.5,0.7], RR:[0.4,0.6]
#   no_depessive: OR:[0.3,0.5], AR:[0.6,1.0], IR:[0.1,0.3], RR:[0.1,0.3]
# 3. "1" for depression, "0" for not_depression
# ==========================
# '/Users/cancui/workspace/virENV/lccanalysissystem/src/main/resources/behaviordata_sim/behaviordata_sim.csv'
def get_interdata_patterns_sim(biodata):
    label_indx = len(biodata[0]) - 1
    interdata = []
    for i in range(0, len(biodata)):
        if biodata[i][label_indx] == 1:
            dep_offerrate = random.choice(range(6, 10))
            dep_acceptrate = random.choice(range(4, 10))
            dep_investrate = random.choice(range(5, 8))
            dep_repayrate = random.choice(range(4, 6))
            interdata = interdata + [[dep_offerrate, dep_acceptrate, dep_investrate, dep_repayrate]]
        else:
            notdep_offerrate = random.choice(range(3, 6))
            notdep_acceptrate = random.choice(range(6, 10))
            notdep_investrate = random.choice(range(1, 4))
            notdep_repayrate = random.choice(range(1, 4))
            interdata = interdata + [[notdep_offerrate, notdep_acceptrate, notdep_investrate, notdep_repayrate]]
    return interdata

#=========================================
# get mixdata patterns
#=========================================
def get_mixdata_patterns(interdata,biodata):
    num_interdata_features=len(interdata[0])-1
    num_biodata_features=len(biodata[0])-1
    mixdata_features=[]
    for i in range(0,len(interdata)):
        mixdata_features=mixdata_features+[biodata[i][0:num_biodata_features]+interdata[i][0:num_interdata_features]]
    return mixdata_features

#=============================
# get data features and labels
#=============================
def get_features_labels(alldata,label_indx,featuresrate):
    alldata_array=np.asarray(alldata)
    train_features, test_features, train_labels, test_labels = train_test_split(alldata_array[:, 0:label_indx],
                                                                                alldata_array[:, label_indx],
                                                                                test_size=featuresrate,
                                                                                random_state=0)
    a={'train_features': train_features,
       'train_labels': train_labels,
       'test_features': test_features,
       'test_labels': test_labels}
    return a