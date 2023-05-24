import multiprocessing
import time
from datetime import datetime
from ppadb.device import Device

from utils import dump_queue


def get_elapsed_memory_usage_by_pid(device: Device, pid: int, queue: multiprocessing.Queue):
    """
    Calculate the cpu usage by the given pid and put it in the multiprocessing queue's dict
    """
    elapsed_memory_usage = {}

    base_test_time = datetime.now()

    # TODO: Make this to fit in the time constraint that are given
    for _ in range(50):
        time.sleep(0.1)

        memory_usage = device.get_meminfo(pid)

        diff_time = datetime.now() - base_test_time

        elapsed_memory_usage[str(diff_time)] = memory_usage.pss / 1024

    queue.put((pid, elapsed_memory_usage))


def get_all_elapsed_memory_usage(device: Device, package_name: str):
    """
    Calculate elapsed memory usage for multiprocessing process
    """
    pids = device.get_pids(package_name)

    processes: list[multiprocessing.Process] = []
    queue: multiprocessing.Queue = multiprocessing.Queue()

    for pid in pids:
        process = multiprocessing.Process(
            target=get_elapsed_memory_usage_by_pid, args=(device, pid, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return dump_queue(queue)
