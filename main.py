import multiprocessing
import time
from datetime import datetime
from ppadb.client import Client as AdbClient
from ppadb.device import Device

# package that we are testing
testing_package = 'com.example.passenger_client'

client = AdbClient(host="127.0.0.1", port=5037)
HERTZ = 100


def list_devices() -> list[Device]:
    return client.devices()


# make sure that the first element of the array is the device that we're testing
devices = list_devices()
device = devices[0]


def dump_queue(queue):
    """
    Empties all pending items in a queue and returns them in a list.
    """
    result = []

    while not queue.empty():
        result.append(queue.get())
    return result


def get_elapsed_cpu_usage_by_pid(pid, queue: multiprocessing.Queue):
    """
    Calculate the cpu usage by the given pid and put it in the multiprocessing queue's dict
    """
    elapsed_cpu_usage = {}

    base_test_time = datetime.now()
    total_cpu_time_before = device.get_total_cpu().total()
    total_process_time_before = device.get_pid_cpu(pid).total()

    for _ in range(100):
        time.sleep(0.1)
        total_cpu_time_after = device.get_total_cpu().total()
        total_process_time_after = device.get_pid_cpu(pid).total()

        # Reference: https://stackoverflow.com/questions/1420426/how-to-calculate-the-cpu-usage-of-a-process-by-pid-in-linux-from-c/1424556#1424556
        cpu_usage = 100 * ((total_process_time_after - total_process_time_before) /
                           (total_cpu_time_after - total_cpu_time_before))
        diff_time = datetime.now() - base_test_time

        elapsed_cpu_usage[str(diff_time)] = cpu_usage

    queue.put((pid, elapsed_cpu_usage))


def get_all_elapsed_cpu_usage():
    """
    Calculate elapsed cpu usage for multiprocessing process
    """
    pids = device.get_pids(testing_package)

    processes: list[multiprocessing.Process] = []
    queue: multiprocessing.Queue = multiprocessing.Queue()

    for pid in pids:
        process = multiprocessing.Process(
            target=get_elapsed_cpu_usage_by_pid, args=(pid, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return dump_queue(queue=queue)


if __name__ == "__main__":

    elapsed_cpu_usage = get_all_elapsed_cpu_usage()
    print(elapsed_cpu_usage)
