import matplotlib.pyplot as plt

# Names of the chaincode functions
functions = ['AddController', 'AddSwitches', 'SubmitProposal', 'EnforcePolicy', 'UpdateTrustScore']

# Transaction costs for each function (in arbitrary units)
transaction_costs = [20, 25, 60, 80, 15]

# Plotting the graph
plt.figure(figsize=(10, 6))
plt.bar(functions, transaction_costs, color=['yellowgreen', 'Orchid', 'Orange', 'SkyBlue', 'Maroon'])

# Graph labels and title
#plt.title('Transaction Cost for Chaincode Function Execution')
plt.xlabel('Chaincode Functions')
plt.ylabel('Transaction Cost (Computational Fee)')

# Adding a grid for better readability
plt.grid(True, axis='y')

# Show the plot
plt.show()
