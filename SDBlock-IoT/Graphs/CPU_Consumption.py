




# create data 



import matplotlib.pyplot as plt 
import numpy as np 
  




x1 = [100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500]

Proposed_Time = [5,7,9,11,14,19,25,31,38,46,54,63,72,82,93]

#ax = plt.subplot(111)
#fig, (ax1, ax2) = plt.subplots(2)

plt.figure(figsize=(8,5))

#plt.title("Execution Time Comparison")

# plot lines 
plt.plot(x1, Proposed_Time, '-ob',label = "OFBlock") 

plt.xlabel('Flow_Mod Rate (Packets/second)', fontsize=15)
plt.ylabel('CPU Consumption (%)', fontsize=15)


plt.tight_layout()

#plt.legend()
plt.grid(axis = 'y')

plt.show()






