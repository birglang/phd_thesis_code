
# CPU Utilization of SDBlock-IoT


import matplotlib.pyplot as plt 
import numpy as np 
  



x1 = [500,1000,1500,2000,2500,3000]

Proposed_CPU = [5,11,18,25,34,42]

FRChain_CPU = [8,15,22,29,40,47]

BlockFlow_CPU = [10,21,33,48,64,71]

BlockSDSec_CPU = [13,25,39,55,68,79]



#ax = plt.subplot(111)
#fig, (ax1, ax2) = plt.subplots(2)

plt.figure(figsize=(8,5))
#plt.title("Verification Time Comparison")

# plot lines
'''
plt.plot(x1, Proposed_Time, '-*r', label = "SDBlock-IoT") 
plt.plot(x1, BlockFlow_Time, '-4b',label = "BlockFlow")
plt.plot(x1, BlockSDSec_Time, '-xg',label = "BlockSDSec")
plt.plot(x1, FRChain_Time, '->y',label = "FRChain")
'''
plt.plot(x1, Proposed_CPU, '-*r', label = "SDBlock-IoT") 
plt.plot(x1, BlockFlow_CPU, '-vb',label = "BlockFlow")
plt.plot(x1, BlockSDSec_CPU, '-xg',label = "BlockSDSec")
plt.plot(x1, FRChain_CPU, '-oy',label = "FRChain")


plt.xlabel('No. of flow mod attack', fontsize=15)
plt.ylabel('CPU Utilization (%)', fontsize=15)

#plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
#plt.legend(["Proposed", "BlockFlow"], loc ="lower right")

plt.legend(["SDBlock-IoT", "BlockFlow","BlockSDSec","FRChain"], loc ="upper left")
plt.tight_layout()

#plt.legend()
plt.grid(axis = 'y')

plt.show()






