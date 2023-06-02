#!/usr/bin/env python3

import shutil
import importlib
import platform
import time
import sys
import subprocess
import select
import tty
import termios
import threading
import keyboard

from lib_getinfo import get_cpu_percent, get_memory_info, get_network_info, get_process_list, NETWORK_DATA
from lib_show import draw_interface

user_input = None

def get_user_input(timeout=5):
    """
    Get user input with a timeout
    """
    # Save the current terminal attributes
    old_settings = termios.tcgetattr(sys.stdin)

    try:
        # Set the input mode to raw
        tty.setcbreak(sys.stdin.fileno())

        # Use select to handle input with a timeout
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        if rlist:
            # Read a single character
            char = sys.stdin.read(1)
            if char == "\x1b":  # Arrow key
                char = sys.stdin.read(2)  # Read the additional escape sequence
            return char
        else:
            return None
    finally:
        # Restore the terminal attributes
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def check_dependencies():
    """
    Check if all required dependencies are installed
    """
    dependencies = [
        "psutil",
        "colorama",
        "asciichartpy",
        "numpy",
        "matplotlib",
        "platform",
        "time",
        "sys",
        "os",
        "subprocess"
    ]

    missing_dependencies = []
    for dependency in dependencies:
        try:
            importlib.import_module(dependency)
        except ImportError:
            missing_dependencies.append(dependency)

    if missing_dependencies:
        print("The following dependencies are missing:")
        for dependency in missing_dependencies:
            print(dependency)
        print("Please install the required dependencies and try again.")
        return False

    return True

def get_OS():
    """
    Get the operating system
    """
    system = platform.system()
    if system == "Windows":
        return "Windows"
    elif system == "Linux":
        return "Linux"
    elif system == "Darwin":
        return "Mac OS"
    else:
        return "Unknown"

# Register the key press handler
#keyboard.on_press(handle_key_press)

def main():

    # get terminal size
    terminal_width, terminal_height = shutil.get_terminal_size()

    # OS detection
    operating_system = get_OS()

    # Check dependencies
    if not check_dependencies():
        return 0

    # Set the refresh rate (in seconds)
    refresh_rate = 4
    start_index = 0
    max_display = terminal_height - 15 #number of line that i use to print the other stuff

    # Run the main loop
    try:
        while True:
            print("The operating system is: {operating_system}")
            
            terminal_width, terminal_height = shutil.get_terminal_size()
            max_display = terminal_height - 15 #number of line that i use to print the other stuff

            # Get the list of processes
            processes = get_process_list()

            # Get process information
            processes = get_process_list()

            # Draw the interface
            draw_interface(processes,start_index,max_display)
            
            # Update the network data
            update_network_data()

            # delay to get the keyboard input(daemon)
            time.sleep(0.01)

            user_input = get_user_input(refresh_rate)
            
            if user_input == "q":
                print("\nExiting...")
                sys.exit(0)
            elif user_input == "[C": #richt arrow
                start_index += max_display
                if start_index >= len(processes):
                    start_index = 0
            elif user_input == "[D": # left arrow
                start_index -= max_display
                if start_index <= 0:
                    start_index = len(processes) - (len(processes) % max_display)

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


# Start the keyboard event capture in a separate thread
keyboard_thread = threading.Thread(target=keyboard.wait)
keyboard_thread.daemon = True
keyboard_thread.start()

# Call the main function
main()
