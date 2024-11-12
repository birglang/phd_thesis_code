import numpy as np
import matplotlib.pyplot as plt


# creating the dataset
data = {'Contract Creation':150149, 'addSwitches()':93419, 'addRule()':140006,
		'deleteRule()':140813}
courses = list(data.keys())
values = list(data.values())

fig = plt.figure(figsize = (8, 5))

# creating the bar plot
plt.bar(courses, values, color ='maroon',
		width = 0.4)

plt.xlabel("Smart Contract Functions", fontsize = 15)
plt.ylabel("Gas Used (Unit Gas)", fontsize = 15)
plt.title("Gas Used by different SC functions")
plt.show()
