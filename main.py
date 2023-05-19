#!/usr/bin/env python3

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
from lib_show import draw_interface, update_network_data

user_input = None

def handle_key_press(event):
    global user_input

    key = event.name
    if key == 'q':
        user_input = 'q'
    elif key == 's':
        user_input = 's'
    elif key == 'd':
        user_input = 'd'

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
    # OS detection
    operating_system = get_OS()

    # Check dependencies
    if not check_dependencies():
        return 0

    # Set the refresh rate (in seconds)
    refresh_rate = 4
    start_index = 0
    max_display = 40

    # Run the main loop
    try:
        while True:
            print("The operating system is: {operating_system}")

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

            # Get user input in a subprocess
            user_input = get_user_input(refresh_rate)

            if user_input == "q":
                print("\nExiting...")
                sys.exit(0)
            elif user_input == "s":
                start_index += max_display
                if start_index >= len(processes):
                    start_index = 0
            elif user_input == "d":
                start_index -= max_display
                if start_index <= 0:
                    start_index = 0

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


# Start the keyboard event capture in a separate thread
keyboard_thread = threading.Thread(target=keyboard.wait)
keyboard_thread.daemon = True
keyboard_thread.start()

# Call the main function
main()
