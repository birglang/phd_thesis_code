import matplotlib.pyplot as plt

# Function names
functions = ['addController()', 'verifyProposal()', 'updateTrustScore()', 'enforcePolicy()']

# Execution times in ms
execution_time = [150, 300, 250, 400]

# Resource costs in arbitrary units
resource_cost = [10, 20, 15, 25]

# Total costs (sum of execution time and resource cost)
total_cost = [160, 320, 265, 425]

# Plotting the graph
plt.figure(figsize=(10, 6))

# Bar chart for execution time
plt.bar(functions, execution_time, color='b', label='Execution Time (ms)')

# Adding resource costs on top of execution time bars
for i in range(len(functions)):
    plt.text(i, execution_time[i] + 5, f'{execution_time[i]}', ha='center', color='b')

# Adding resource cost bars on top of execution time bars
plt.bar(functions, resource_cost, bottom=execution_time, color='r', label='Resource Cost')

# Adding total costs
for i in range(len(functions)):
    plt.text(i, total_cost[i] + 5, f'{total_cost[i]}', ha='center', color='r')

plt.title('Transaction Costs for Chaincode Functions')
plt.xlabel('Chaincode Functions')
plt.ylabel('Cost (ms or arbitrary units)')
plt.legend()
plt.show()
