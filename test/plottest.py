import matplotlib.pyplot as plt
#=================
#polt sample data
#=================
sample_x=[[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]]
sample_y=[[1,2,3,4,5],[2,4,6,8,10],[3,6,9,12,15]]
plt.plot(sample_x[0],sample_y[0],'ro-',sample_x[1],sample_y[1],'bs--',sample_x[2],sample_y[2],'go-')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
