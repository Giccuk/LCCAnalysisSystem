import random,re
import numpy as np
from sklearn import linear_model
from numpy import array

datasrc="/Users/cancui/workspace/virENV/lccbehavioranalysis/src/main/resources/seeds/seeds_dataset.txt"
with open(datasrc,"r") as seedsdatafile:
	  seedsdatalines=seedsdatafile.readlines()
seedsdata=[]
for eachline in seedsdatalines:
	rresult=eachline.replace("\t",",")
	seedsdata=seedsdata+[rresult]

seedsfeatures=[]
seedslabels=[]
pattern_feature=re.compile(r'(\d+\.*\d*),')
pattern_label=re.compile(r',(\d)\n')
for linei in range(len(seedsdata)):
	if linei<(len(seedsdata)-1):
		featureresult=re.findall(pattern_feature,seedsdata[linei])
		seedsfeatures=seedsfeatures+[map(float,featureresult)]
		labelresult=re.findall(pattern_label,seedsdata[linei])
		seedslabels=seedslabels+map(float,labelresult)
	else:
		featureresult=re.findall(pattern_feature,seedsdata[linei])
		seedsfeatures=seedsfeatures+[map(float,featureresult)]
		lenlastline=len(seedsdata[linei])
		pos=lenlastline-1
		seedslabels=seedslabels+[float(seedsdata[linei][pos])]
