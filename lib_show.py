import sys
import os
import subprocess
import time
import sys
import asciichartpy
import matplotlib.pyplot as plt
import numpy as np
from watchgod import watch
import colorama
from colorama import Fore, Style

from lib_getinfo import (
    get_cpu_percent, 
    get_memory_info, 
    get_network_info, 
    get_process_list,
    format_bytes,
    NETWORK_DATA
)

NETWORK_DATA = []

colorama.init()

def draw_interface(processes, start, max_disp, show_process=True, show_network=True):
    """
    Draw the interface with process and network information
    """
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    if show_process:
        draw_process_info(processes,start,max_disp)

    if show_network:
        network_info = get_network_info()
        draw_network_info(network_info)

def draw_process_info(processes, start_index=0, max_display=10):
    """
    Draw process information with scrolling support
    """
    end_index = start_index + max_display

    print("=" * 100)
    print("| {0:<6s} | {1:<30s} | {2:<8s} | {3:<8s} |".format("PID", "Name", "CPU", "Memory"))
    print("-" * 100)
    for index, process in enumerate(processes[start_index:end_index], start=start_index):
        pid = str(process["pid"])
        name = process["name"]
        cpu = "{:.2f}%".format(process["cpu_percent"])
        memory = format_bytes(process["memory_info"].rss)

        print("| {0:<6s} | {1:<30s} | {2:<8s} | {3:<8s} |".format(pid, name, cpu, memory))

    print("-" * 100)
    print(f"Showing processes {start_index+1}-{end_index} of {len(processes)}")

    if end_index < len(processes):
        print("Press 's' to scroll up to view more processes.")
        print("Press 'd' to scroll down to view more processes.")
    print("=" * 100)

    return start_index + max_display if end_index < len(processes) else None

def draw_network_info(network_info):
    """
    Draw network information
    """
    print("Network Information:")
    print("| {0:<15s} | {1:<15s} |".format("Download", "Upload"))
    print("-" * 34)
    print("| {0:<15s} | {1:<15s} |".format(format_bytes(network_info["received"]), format_bytes(network_info["sent"])))

    print("=" * 80)
    #draw_network_graph_CLI()

def draw_network_graph_gui():
    """
    Draw the network data graph
    """
    plt.figure()
    plt.xlabel("Time (s)")
    plt.ylabel("Network Data (B)")
    plt.title("Network Data Graph")

    # Get the data points from the network_data list
    data_points = [(t, received, sent) for t, received, sent in NETWORK_DATA]

    # Convert the data points to numpy arrays for plotting
    time_points = np.array([t for t, _, _ in data_points])
    received_points = np.array([received for _, received, _ in data_points])
    sent_points = np.array([sent for _, _, sent in data_points])

    # Plot the received and sent data points
    plt.plot(time_points, received_points, label="Received")
    plt.plot(time_points, sent_points, label="Sent")

    plt.legend()
    plt.show()

def draw_network_graph_CLI():
    """
    Draw network graph using text-based visualization
    """
    timestamps = [t for t, _, _ in NETWORK_DATA]
    received_data = [received for _, received, _ in NETWORK_DATA]
    sent_data = [sent for _, _, sent in NETWORK_DATA]

    chart = asciichartpy.plot([received_data, sent_data], {'height': 10})
    print(f"{Fore.RED}{chart}{Style.RESET_ALL}")

def update_network_data():
    """
    Update the network data
    """
    network_info = get_network_info()
    current_time = time.time()
    received = network_info["received"]
    sent = network_info["sent"]

    NETWORK_DATA.append((current_time, received, sent))

def run():
    # Set the refresh rate (in seconds)
    refresh_rate = 1
    
    # Run the main loop
    try:
        while True:
            # Get process information
            processes = get_process_list()


            # Draw the interface
            draw_interface(processes)

            # Update the network data
            update_network_data()

            # Wait for the specified refresh rate
            time.sleep(refresh_rate)

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


if __name__ == "__main__":
    run()