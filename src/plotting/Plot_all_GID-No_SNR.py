
# coding: utf-8

# In[ ]:

import csv
import numpy as np

with open('15_1SS_NO-SU.csv') as f:
    MU_groups = [{k:v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]


# In[ ]:

import matplotlib.pyplot as plt

colors = {}
handles = {}

for i in MU_groups:
    for mac in i['addrs'].strip("[").replace("]", "").replace(" ", "").split(","):
        if mac in colors:
            continue
            
        colors[mac] = np.random.rand(3,1)
    
#print colors
print len(MU_groups)
width = 0.5
step = 4*width
index = 0
j = 0


plt.style.use("ggplot")
plt.clf()
MU_Group_iters = {} 
MU_Group_iter2 = {}
varx = []
MU_Group_iter_array = []

for i in MU_groups:
    if not i['Gid'] in MU_Group_iter2:
        MU_Group_iter2[i['Gid']] = 1
    else :
        MU_Group_iter2[i['Gid']]+=1
print MU_Group_iter2

for i in MU_groups:
    if not i['Gid'] in MU_Group_iters:
        MU_Group_iters[i['Gid']] = 1
        snrs = i['SNRs'].strip("[").replace("]", "").replace(" ", "").split(",")
        macs = i['addrs'].strip("[").replace("]", "").replace(" ", "").split(",")
        varx.append(index+(j*width/2))
        for j in range(len(macs)):
            if macs[j] in handles :
                plt.bar(index+(j*width), MU_Group_iter2[i['Gid']], width, color = colors[macs[j]])
            else:
                handles[macs[j]] = plt.bar(index+(j*width), MU_Group_iter2[i['Gid']], width, color = colors[macs[j]])
        index += step
        MU_Group_iter_array.append(i['Gid'])
    else:
        MU_Group_iters[i['Gid']]+= 1

        
handles = [handles[mac] for mac in colors]
labels = [mac[len(mac)-6:len(mac)-1] for mac in colors]

#plt.ylim(0,40)
plt.legend(handles, labels, loc ='upper right', ncol = 5)
#print (varx)
#print 'delimiter'
#print (MU_Group_iter_array)

plt.xticks(varx, MU_Group_iter_array)
plt.xlabel("Group ID")
plt.ylabel("Number of Frames for GID")
plt.show()


# In[ ]:



