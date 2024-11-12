import matplotlib.pyplot as plt
# Plotting the data as a bar graph
plt.figure(figsize=(12, 8))
width = 4  # width of the bars

# Time in seconds
time = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 122, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260]

# CPU consumption with the proposed method
cpu_with_method = [26, 27, 26, 27, 28, 29, 29, 29, 29, 42, 41, 37, 30, 29, 31, 30, 29, 28, 28, 29, 29, 28, 28, 28, 29, 29, 29]

# CPU consumption without the proposed method
cpu_without_method = [24, 25, 27, 27, 26, 31, 30, 31, 32, 39, 51, 56, 67, 62, 60, 58, 66, 72, 78, 85, 95, 100, 100, 100, 100, 100, 100]


# Creating bar positions
time_pos = [t - width/2 for t in time]  # Positioning for the first set of bars

plt.bar(time_pos, cpu_with_method, width=width, color='b', label='CPU Consumption with Cross-DistBlock')
plt.bar(time, cpu_without_method, width=width, color='r', alpha=0.6, label='CPU Consumption without Cross-DistBlock')

# Adding titles and labels
plt.title('CPU Consumption vs. Time', fontsize=20)
plt.xlabel('Time (s)', fontsize=20)
plt.ylabel('CPU Consumption (%)', fontsize=20)
plt.axvline(x=80, color='y', linestyle='--', label='First Attack Start')
plt.axvline(x=122, color='g', linestyle='--', label='Stabilization Start')
plt.axvline(x=130, color='y', linestyle='--', label='Second Attack Start')
plt.legend()

# Show the plot
plt.grid(True)
plt.show()
