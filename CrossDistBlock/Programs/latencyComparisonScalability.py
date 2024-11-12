import matplotlib.pyplot as plt
import numpy as np

# Number of proposal requests
proposal_requests = np.array([1000, 10000, 20000, 30000, 40000, 50000])

# Latency data (in ms) for each method
latency_proposed = np.array([45, 90, 147, 196, 240, 297])
latency_bcs = np.array([60, 123, 180, 232, 345, 446])
latency_bmc_sdn = np.array([75, 130, 185, 280, 330, 380])
latency_frchain = np.array([43, 100, 191, 304, 380, 470])

# Plotting the data
plt.figure(figsize=(10, 6))

plt.plot(proposal_requests, latency_proposed, 'x-', label='Cross-DistBlock', color='red')
plt.plot(proposal_requests, latency_bcs, 'D-', label='BCS', color='purple')
plt.plot(proposal_requests, latency_bmc_sdn, '^-', label='BMC-SDN', color='orange')
plt.plot(proposal_requests, latency_frchain, 'o-', label='FRChain', color='blue')

# Graph labels and title
plt.title('Latency vs Number of Proposal Requests', fontsize=20)
plt.xlabel('Number of Proposal Requests', fontsize=20)
plt.ylabel('Latency (ms)', fontsize=20)
plt.legend()

# Display grid
plt.grid(True)

# Show plot
plt.show()
