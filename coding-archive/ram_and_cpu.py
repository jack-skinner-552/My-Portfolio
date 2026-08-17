import psutil
import matplotlib.pyplot as plt

# Initialize a figure to plot RAM and CPU usage
fig, ax = plt.subplots()

# Set the x-axis limits to 0-100, and the y-axis limits to 0-100
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

# Initialize the RAM and CPU usage lines
ram_line, = ax.plot([], [], label='RAM')
ram_bar = ax.bar([], [], width=0.9)
cpu_line, = ax.plot([], [], label='CPU')
cpu_bar = ax.bar([], [], width=0.9)

# Add a legend to the plot
ax.legend()

# Start an infinite loop to update the plot
while True:
    # Get the current RAM and CPU usage as percentages
    ram_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent()

    # Append the new RAM and CPU usage to the lines
    ram_line.set_xdata(list(range(len(ram_line.get_ydata()), len(ram_line.get_ydata())+1)))
    ram_line.set_ydata(list(ram_line.get_ydata()) + [ram_usage])
    ram_bar.patches.append(ax.bar(len(ram_bar.patches), ram_usage, width=0.9, color='blue')[0])
    cpu_line.set_xdata(list(range(len(cpu_line.get_ydata()), len(cpu_line.get_ydata())+1)))
    cpu_line.set_ydata(list(cpu_line.get_ydata()) + [cpu_usage])
    cpu_bar.patches.append(ax.bar(len(cpu_bar.patches), cpu_usage, width=0.9, color='orange')[0])

    # Update the plot
    fig.canvas.draw()

    # Pause for a short time to avoid overwhelming the system
    plt.pause(0.1)
