
# Controller Update Time Comparison


import matplotlib.pyplot as plt 
import numpy as np 
  

'''
# Average of 52ms is required during normal scenario for Controller update
# Therefore, for attack scenario, start the updation time as

Proposed_Time = 18
FRChain_Time = 25
BlockFlow_Time = 32
BlockSDSec_Time = 37
'''

x1 = [10,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600,2700,2800,2900,3000]

Proposed_Time = [18,23,30,39,50,63,78,95,114,135,158,183,210,239,270,303,338,375,414,455,498,543,590,639,690,743,798,855,914,975,1023]
FRChain_Time = [25,31,40,52,67,85,106,130,157,187,220,256,295,337,382,430,481,535,592,652,715,781,850,922,997,1075,1156,1240,1327,1417,1510]
BlockFlow_Time = [37,48,67,94,129,172,223,282,349,424,507,598,697,804,919,1042,1173,1312,1459,1614,1777,1948,2127,2314,2509,2712,2923,3142,3369,3604,3847]
BlockSDSec_Time = [32,41,56,77,104,137,176,221,272,329,392,461,536,617,704,797,896,1001,1112,1229,1352,1481,1616,1757,1904,2057,2216,2381,2552,2729,2912]

#ax = plt.subplot(111)
#fig, (ax1, ax2) = plt.subplots(2)

plt.figure(figsize=(8,5))
#plt.title("Controller Update Time Comparison")

# plot lines
'''
plt.plot(x1, Proposed_Time, '-*r', label = "SDBlock-IoT") 
plt.plot(x1, BlockFlow_Time, '-4b',label = "BlockFlow")
plt.plot(x1, BlockSDSec_Time, '-xg',label = "BlockSDSec")
plt.plot(x1, FRChain_Time, '->y',label = "FRChain")
'''
plt.plot(x1, Proposed_Time, '-or', label = "SDBlock-IoT") 
plt.plot(x1, BlockFlow_Time, '-ob',label = "BlockFlow")
plt.plot(x1, BlockSDSec_Time, '-og',label = "BlockSDSec")
plt.plot(x1, FRChain_Time, '-oy',label = "FRChain")


plt.xlabel('No. of flow mod attack', fontsize=15)
plt.ylabel('Network Update Time (ms)', fontsize=15)

#plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
#plt.legend(["Proposed", "BlockFlow"], loc ="lower right")

plt.legend(["SDBlock-IoT", "BlockFlow","BlockSDSec","FRChain"], loc ="upper left")
plt.tight_layout()

#plt.legend()
plt.grid(axis = 'y')

plt.show()






