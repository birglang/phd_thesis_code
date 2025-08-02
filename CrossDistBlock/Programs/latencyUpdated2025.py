import matplotlib.pyplot as plt
import numpy as np

# Number of proposal requests
proposal_requests = np.array([1000, 10000, 20000, 30000, 40000, 50000])

# Latency data (in ms)
latency_proposed = np.array([45, 90, 147, 196, 240, 297])
latency_bcs = np.array([60, 123, 180, 232, 345, 446])
latency_bmc_sdn = np.array([75, 130, 185, 280, 330, 380])
latency_frchain = np.array([43, 100, 191, 304, 380, 470])
latency_bdac = np.array([72, 125, 210, 298, 385, 490])
latency_smartblock = np.array([58, 110, 175, 260, 340, 420])

# Plotting
plt.figure(figsize=(12, 7))

plt.plot(proposal_requests, latency_proposed, 'x-', label='Cross-DistBlock', color='red')
plt.plot(proposal_requests, latency_bcs, 'D-', label='BCS', color='purple')
plt.plot(proposal_requests, latency_bmc_sdn, '^-', label='BMC-SDN', color='orange')
plt.plot(proposal_requests, latency_frchain, 'o-', label='FRChain', color='blue')
plt.plot(proposal_requests, latency_bdac, 's-', label='B-DAC', color='green')
plt.plot(proposal_requests, latency_smartblock, 'v-', label='SmartBlock-SDN', color='brown')

plt.title('Latency vs Number of Proposal Requests', fontsize=20)
plt.xlabel('Number of Proposal Requests', fontsize=16)
plt.ylabel('Latency (ms)', fontsize=16)
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()
