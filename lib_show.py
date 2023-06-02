import shutil
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

    draw_general_info()
def draw_network_info(network_info):
    """
    Draw network information
    """
    terminal_width, _ = shutil.get_terminal_size()
    download = format_bytes(network_info["received"])
    upload = format_bytes(network_info["sent"])

    print("Network Information:")
    print("-" * terminal_width)
    print("| {0:<15s} | {1:<15s} |".format("Download", "Upload"))
    print("| {0:<15s} | {1:<15s} |".format(download, upload))
    print("-" * terminal_width)

    #draw_network_graph_CLI()

def update_network_data():
    """
    Update the network data
    """
    network_info = get_network_info()
    current_time = time.time()
    received = network_info["received"]
    sent = network_info["sent"]

    NETWORK_DATA.append((current_time, received, sent))
    
def draw_general_info():
    """
    Draw process information with scrolling support, sorted by CPU power usage
    """
    terminal_width, _ = shutil.get_terminal_size()

    cpu_percent= get_cpu_percent()
    cpu_percent_generale = sum(cpu_percent) / len(cpu_percent)
    memory_usage = get_memory_info()

def draw_process_info(processes, start_index=0, max_display=10):
    terminal_width, terminal_height = shutil.get_terminal_size()
    sorted_processes = sorted(processes, key=lambda p: p["cpu_percent"], reverse=True)

    end_index = start_index + max_display
    max_pid_length = max(len(str(process["pid"])) for process in sorted_processes[start_index:end_index])

    print_header(terminal_width, max_pid_length)
    print_processes(sorted_processes, start_index, end_index)
    print_footer(start_index, end_index, sorted_processes)

    return start_index + max_display if end_index < len(sorted_processes) else None

def print_header(terminal_width, max_pid_length):
    print("=" * 70)
    print("|  {0:<{pid_width}s}  | {1:<30s}          | {2:<8s}      | {3:<14s}         |".format(
        Fore.YELLOW + "PID" + Style.RESET_ALL, Fore.YELLOW + "Name" + Style.RESET_ALL, Fore.YELLOW + "CPU" + Style.RESET_ALL, Fore.YELLOW + "Memory" + Style.RESET_ALL,
        pid_width=str(max_pid_length)))

def print_processes(processes, start_index, end_index):
    print("-" * 70)

    max_pid_length = max(len(str(process["pid"])) for process in processes[start_index:end_index])

    for index, process in enumerate(processes[start_index:end_index], start=start_index):
        pid = str(process["pid"]).ljust(max_pid_length)                                                                                                                                                                                                                                                                                                                                    
        name = process["name"].ljust(30)                                                                                                                                                                                                                                                                                                                                                   
        cpu = "{:.2f}%".format(process["cpu_percent"]).ljust(8)                                                                                                                                                                                                                                                                                                                            
        memory = format_bytes(process["memory_info"].rss).ljust(14)                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                                                                                           
        print("| {0} | {1} | {2} | {3} |".format(Fore.CYAN + pid + Style.RESET_ALL, Fore.CYAN + name + Style.RESET_ALL, Fore.RED + cpu + Style.RESET_ALL, Fore.RED + memory + Style.RESET_ALL))                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                                                                                           
def print_footer(start_index, end_index, processes):                                                                                                                                                                                                                                                                                                                                       
    terminal_width, _ = shutil.get_terminal_size()                                                                                                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                                                                                                                                           
    total_processes = len(processes)                                                                                                                                                                                                                                                                                                                                                       
    print("-" * 70)                                                                                                                                                                                                                                                                                                                                                                        
    print(Fore.YELLOW+"Showing processes {start}-{end} of {total}".format(                                                                                                                                                                                                                                                                                                                 
        start=start_index + 1, end=min(end_index, total_processes), total=total_processes)+ Style.RESET_ALL)                                                                                                                                                                                                                                                                               
    print("=" * 70)     
