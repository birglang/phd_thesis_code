import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

# set width of bar
barWidth = 0.15
fig = plt.subplots(figsize =(8,5))

# set height of bar
OFBlock = [710816,1410846,2110876,2810906,3510936,4210966]
BlockFlow = [910814,1710834,3001634,3990634,4713634,5810934]
BlockSDSec = [810634,1610634,2410834,3010634,3810934,4810634]

# Set position of bar on X axis
br1 = np.arange(len(OFBlock))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

# Make the plot
plt.bar(br1, OFBlock, color='#D83D1C', width = barWidth,
		edgecolor ='black', label ='SDBlock-IoT')
plt.bar(br2, BlockFlow, color ='#347B27', width = barWidth,
		edgecolor ='black', label ='BlockFlow')
plt.bar(br3, BlockSDSec, color ='black', width = barWidth,
		edgecolor ='black', label ='BlockSDSec')
'''
plt.bar(br1, OFBlock, color ='r', width = barWidth,
		edgecolor ='grey', label ='OFBlock')
plt.bar(br2, BlockFlow, color ='g', width = barWidth,
		edgecolor ='grey', label ='BlockFlow')
plt.bar(br3, BlockSDSec, color ='b', width = barWidth,
		edgecolor ='grey', label ='BlockSDSec')
'''
# Adding Xticks
plt.title("Transaction Cost Comparison")
plt.xlabel('No of Flows',  fontsize = 15)
plt.ylabel('Gas Cost', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(OFBlock))],
		['500', '1000', '1500', '2000', '2500', '3000'])

plt.grid(axis = 'y')
plt.legend()
plt.show()
