import psutil
import time
import math

NETWORK_DATA = []
NETWORK_DATA_DURATION = 60  # Duration in seconds
PREVIOUS_NETWORK_BYTES = None

def format_bytes(bytes):
    """
    Format bytes to a human-readable format
    """
    if bytes == 0:
        return "0 B"
    sizes = ["B", "KB", "MB", "GB", "TB"]
    i = int(math.floor(math.log(bytes, 1024)))
    formatted_bytes = round(bytes / (1024 ** i), 2)
    return f"{formatted_bytes} {sizes[i]}"

def get_cpu_percent():
    """
    Get CPU usage percentage for each core
    """
    return psutil.cpu_percent(percpu=True)

def get_memory_info():
    """
    Get memory usage information
    """
    memory_info = psutil.virtual_memory()
    return {
        'total': memory_info.total,
        'available': memory_info.available,
        'percent': memory_info.percent,
        'used': memory_info.used,
        'free': memory_info.free
    }

def get_network_info_v2(): #give number of bit since up
    """
    Get network information
    """
    network_info = psutil.net_io_counters()
    received = network_info.bytes_recv
    sent = network_info.bytes_sent

    current_time = time.time()

    # Remove outdated network data
    NETWORK_DATA[:] = [(t, recv, sent) for t, recv, sent in NETWORK_DATA if current_time - t <= NETWORK_DATA_DURATION]

    NETWORK_DATA.append((current_time, received, sent))

    max_data = max(max(received for _, received, _ in NETWORK_DATA), max(sent for _, _, sent in NETWORK_DATA))

    unit = "B"
    if max_data >= 1024:
        unit = "KiB"
        max_data /= 1024
    if max_data >= 1024:
        unit = "MiB"
        max_data /= 1024
    if max_data >= 1024:
        unit = "GiB"
        max_data /= 1024

    return {"received": received, "sent": sent, "unit": unit}

def get_network_info():
    """
    Get network information
    """
    global PREVIOUS_NETWORK_BYTES

    network_info = {}
    network_stats = psutil.net_io_counters()

    # Calculate the difference in network bytes
    if PREVIOUS_NETWORK_BYTES is not None:
        network_info["received"] = network_stats.bytes_recv - PREVIOUS_NETWORK_BYTES[0]
        network_info["sent"] = network_stats.bytes_sent - PREVIOUS_NETWORK_BYTES[1]
    else:
        network_info["received"] = 0
        network_info["sent"] = 0

    # Update the previous network bytes
    PREVIOUS_NETWORK_BYTES = (network_stats.bytes_recv, network_stats.bytes_sent)

    return network_info

def get_process_list():
    """
    Get the list of processes
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info', 'status']):
        process = {
            'pid': proc.info['pid'],
            'name': proc.info['name'],
            'cpu_percent': proc.info['cpu_percent'],
            'memory_info': proc.info['memory_info'],
            'memory_percent': proc.info['memory_percent'],
            'status': proc.info['status']
        }
        processes.append(process)
    return processes
