import matplotlib.pyplot as plt

# Data
num_proposals = [10, 50, 100, 150, 200, 300, 400, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000]
total_latency = [28.5, 138.5, 277.0, 416.0, 555.0, 833.0, 1110.0, 1389.0, 2789.0, 4175.0, 5560.0, 6942.0, 8342.0, 9725.0, 11125.0, 12510.0, 13907.0, 15292.0, 16614.0]
throughput = [0.351, 0.361, 0.361, 0.361, 0.360, 0.360, 0.360, 0.360, 0.359, 0.359, 0.360, 0.360, 0.360, 0.360, 0.360, 0.360, 0.359, 0.359, 0.361]

# Plotting
fig, ax1 = plt.subplots()

# Plotting Total Latency
color = 'tab:red'
ax1.set_xlabel('Number of Proposals')
ax1.set_ylabel('Total Latency (ms)', color=color)
ax1.plot(num_proposals, total_latency, color=color, marker='o', label='Total Latency')
ax1.tick_params(axis='y', labelcolor=color)

# Create a second y-axis for throughput
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Throughput (Proposals/ms)', color=color)
ax2.plot(num_proposals, throughput, color=color, marker='x', label='Throughput')
ax2.tick_params(axis='y', labelcolor=color)

# Adding title and legend
fig.suptitle('Total Latency and Throughput vs Number of Proposals')
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='lower right')

# Show plot
plt.show()
