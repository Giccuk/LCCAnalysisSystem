import numpy as np
from sklearn.cluster import KMeans

#===============================================================================================
#name:label_biodata
#input: num_clusters,interdata_patterns,bio_patterns
#output: biodata
#function: 1. cluster seperate samples into different sets on the basis of their interaction data
#          2. Use the clustering resuluts to label sample's biophysical data
#================================================================================================
def label_biodata(num_clusters,interdata_patterns,bioata_patterns):
    #build interdata features
    interdata_features=np.array([np.zeros(len(interdata_patterns[0]))])
    for i in interdata_patterns:
        interdata_features=np.append(interdata_features,[i],axis=0)
    interdata_features=np.delete(interdata_features,0,0)
    #do clustering on interdata features(kmeans)
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(interdata_features)
    interdata_km_labels=kmeans.labels_
    #kresult=kmeans.predict(interdata_sim_features)
    #build divided mixdata
    biodata=[]
    for i in range(0,len(interdata_km_labels)):
        biodata=biodata+[bioata_patterns[i]+[interdata_km_labels[i]]]
    '''      
    print stats.ttest_ind(kresult,inter_test_labels)
    print accuracy_score(kresult,inter_test_labels)
    print metrics.adjusted_rand_score(kresult,inter_test_labels)
    '''
    return biodata
#================================
# PCA 
#================================
'''
from sklearn.decomposition import PCA
#pcadata = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
def pca_data
np_mixdata=np.array(mixdata)
pca_mixdata=np_mixdata[:,0:14]
pca = PCA(n_components=2)
pca.fit(pca_mixdata)
PCA(copy=True, iterated_power='auto', n_components=2, random_state=None,svd_solver='auto', tol=0.0, whiten=False)
print(pca.explained_variance_ratio_) 
'''