import matplotlib.pyplot as plt

# Time in seconds
time = [0, 10, 20, 30, 40, 50, 60, 70, 80, 85, 100, 110, 120, 130, 147, 150, 160, 170, 180, 185, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310]

# Existing Methods
latency_with_method = [26, 27, 26, 27, 28, 29, 100, 222, 342, 475, 667, 886, 1010, 743, 31, 30, 29, 28, 28, 29, 29, 28, 28, 28, 29, 29, 29, 29, 28, 28, 29, 29]
BCS = [65, 69, 58, 57, 52, 56, 201, 324, 445, 545, 631, 746, 812, 943, 1001, 822, 665, 434, 355, 111, 123, 111, 144, 111, 120, 125, 119, 354, 491, 521, 591, 629]
BMC_SDN = [81, 82, 83, 82, 85, 89, 421, 571, 742, 875, 937, 1086, 1110, 1243, 1301, 1422, 1380, 1229, 1090, 819, 771, 513, 314, 181, 190, 185, 259, 454, 511, 721, 874, 929]
FRChain = [101, 112, 113, 102, 101, 103, 521, 771, 942,1175, 1337, 1586, 1510, 1343,1201, 1122, 1080, 929, 890, 719, 671, 513, 410, 311, 218, 225, 359, 525, 728, 928, 1179, 1229]

# New Methods: Synthetic Data
B_DAC = [38, 39, 38, 40, 41, 42, 150, 260, 395, 505, 588, 715, 819, 701, 510, 400, 365, 310, 300, 270, 245, 235, 220, 210, 200, 205, 215, 220, 225, 230, 235, 240]
Smartblock_sdn = [49, 48, 47, 46, 48, 49, 310, 470, 625, 740, 889, 950, 1030, 925, 730, 690, 660, 610, 590, 530, 490, 420, 390, 355, 330, 345, 366, 388, 405, 422, 460, 485]

# Plotting
plt.figure(figsize=(14, 9))
plt.plot(time, latency_with_method, marker='o', linestyle='-', color='b', label='Cross-DistBlock')
plt.plot(time, BCS, marker='x', linestyle='--', color='k', label='BCS')
plt.plot(time, BMC_SDN, marker='o', linestyle='--', color='g', label='BMC-SDN')
plt.plot(time, FRChain, marker='x', linestyle='--', color='r', label='FRChain')
plt.plot(time, B_DAC, marker='o', linestyle='-.', color='m', label='B_DAC')
plt.plot(time, Smartblock_sdn, marker='x', linestyle='-.', color='c', label='Smartblock_sdn')

# Vertical lines for attack points
plt.axvline(x=50, color='y', linestyle='--', label='First Attack Start')
plt.axvline(x=250, color='orange', linestyle='--', label='Second Attack Start')

# Title and labels
plt.title('Network Latency Comparison During DDoS Attack', fontsize=20)
plt.xlabel('Time (s)', fontsize=16)
plt.ylabel('Latency (ms)', fontsize=16)
plt.grid(True)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()

