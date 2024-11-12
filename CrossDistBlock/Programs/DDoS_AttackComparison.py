
import matplotlib.pyplot as plt

# Time in seconds
time = [0, 10, 20, 30, 40, 50, 60, 70, 80, 85, 100, 110, 120, 130, 147, 150, 160, 170, 180, 185, 200, 210, 220, 230, 240, 250, 260,270, 280, 290, 300,310]

# Latency in milliseconds with the proposed method
latency_with_method = [26, 27, 26, 27, 28, 29, 100, 222, 342, 475, 667, 886, 1010, 743,31, 30, 29, 28, 28, 29, 29, 28, 28, 28, 29, 29, 29, 29, 28, 28, 29, 29]

# Latency in milliseconds without the proposed method
#latency_without_method = [24, 25, 27, 27, 26, 31,230, 569, 987, 1402, 2011, 2710, 3501, 4402, 5440, 6502, 7710, 9070, 13480, 13290, 13003, 13000, 12821, 12795, 12643, 12569, 13814, 14305, 14921, 15700, 16800,18023]

# Latency in milliseconds BCS
BCS = [65, 69, 58, 57, 52, 56, 201, 324, 445, 545, 631, 746, 812, 943, 1001, 822, 665, 434, 355, 111, 123, 111, 144, 111, 120, 125, 119, 354, 491, 521, 591, 629]


# Latency in milliseconds BMC-SDN
BMC_SDN = [81, 82, 83, 82, 85, 89, 421, 571, 742, 875, 937, 1086, 1110, 1243, 1301, 1422, 1380, 1229, 1090, 819, 771, 513, 314, 181, 190, 185, 259, 454, 511, 721, 874, 929]


# Latency in milliseconds FRChain
FRChain = [101, 112, 113, 102, 101, 103, 521, 771, 942,1175, 1337, 1586, 1510, 1343,1201, 1122, 1080, 929, 890, 719, 671, 513, 410, 311, 218, 225, 359, 525, 728, 928, 1179, 1229]


# Plotting the data
plt.figure(figsize=(12, 8))
plt.plot(time, latency_with_method, marker='o', linestyle='-', color='b', label='Cross-DistBlock')
#plt.plot(time, latency_without_method, marker='x', linestyle='--', color='r', label='Latency without Proposed Method')

plt.plot(time, BCS, marker='x', linestyle='--', color='k', label='BCS' )
plt.plot(time, FRChain, marker='o', linestyle='--', color='g', label='BMC-SDN')
plt.plot(time, BMC_SDN, marker='x', linestyle='--', color='r', label='FRChain')


# Adding titles and labels
plt.title('Network Latency vs. Time', fontsize=20)
plt.xlabel('Time (ms)', fontsize=20)
plt.ylabel('Latency (ms)', fontsize=20)
plt.axvline(x=50, color='y', linestyle='--', label='First Attack Start') # gone upto 147 ms
#plt.axvline(x=147, color='g', linestyle='--', label='Stabilization Start')
plt.axvline(x=250, color='y', linestyle='--', label='Second Attack Start')
plt.legend()

# Show the plot
plt.grid(True)
plt.show()




