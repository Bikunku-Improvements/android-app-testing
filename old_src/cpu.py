import multiprocessing
import time
from ppadb.device import Device
from datetime import datetime

from utils import dump_queue


def get_elapsed_cpu_usage_by_pid(device: Device, pid: int, queue: multiprocessing.Queue):
    """
    Calculate the cpu usage by the given pid and put it in the multiprocessing queue's dict
    """
    elapsed_cpu_usage = {}

    base_test_time = datetime.now()
    total_cpu_time_before = device.get_total_cpu().total()
    total_process_time_before = device.get_pid_cpu(pid).total()

    # TODO: Make this to fit in the time constraint that are given
    for _ in range(100):
        time.sleep(0.1)
        total_cpu_time_after = device.get_total_cpu().total()
        total_process_time_after = device.get_pid_cpu(pid).total()

        # Reference: https://stackoverflow.com/questions/1420426/how-to-calculate-the-cpu-usage-of-a-process-by-pid-in-linux-from-c/1424556#1424556
        cpu_usage = 100 * ((total_process_time_after - total_process_time_before) /
                           (total_cpu_time_after - total_cpu_time_before))

        total_cpu_time_before, total_process_time_before = total_cpu_time_after, total_process_time_after
        diff_time = datetime.now() - base_test_time

        elapsed_cpu_usage[str(diff_time)] = cpu_usage

    queue.put((pid, elapsed_cpu_usage))


def get_all_elapsed_cpu_usage(device: Device, package_name: str):
    """
    Calculate elapsed cpu usage for multiprocessing process
    """
    pids = device.get_pids(package_name)

    processes: list[multiprocessing.Process] = []
    queue: multiprocessing.Queue = multiprocessing.Queue()

    for pid in pids:
        process = multiprocessing.Process(
            target=get_elapsed_cpu_usage_by_pid, args=(device, pid, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return dump_queue(queue=queue)
