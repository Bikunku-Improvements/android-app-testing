import time
from ppadb.client import Client as AdbClient

testing_package = 'com.example.passenger_client'

client = AdbClient(host="127.0.0.1", port=5037)
HERTZ = 100

def list_devices():
  return client.devices()

if __name__ == "__main__":
  # make sure that the first element of the array is the device that we're testing
  devices = list_devices()
  chosen_device = devices[0]

  # # get pids
  # pids = chosen_device.get_pids(testing_package)

  # # get cpu process for every pid
  # cpu_processes = []
  # for pid in pids:
  #   cpu_processes.append(chosen_device.get_pid_cpu(pid))

  # # get total cpu usage from every cpu processes
  # cpu_usage_percentages_total = 0
  # for cpu_process in cpu_processes:
  #   total_time = cpu_process.total()
  #   seconds = cpu_process.utime - (cpu_process.stime / HERTZ)
  #   cpu_usage = 100 * ((total_time / HERTZ) / seconds)
  #   cpu_usage_percentages_total += cpu_usage

  # print(f"cpu_usage: {cpu_usage_percentages_total}%")
  
  # I think this works?
  # Reference: https://stackoverflow.com/questions/1420426/how-to-calculate-the-cpu-usage-of-a-process-by-pid-in-linux-from-c/1424556#1424556
  elapsed_cpu_usage = []
  pid = chosen_device.get_pid(testing_package)
  total_time_before = chosen_device.get_total_cpu().total()
  total_jiffy_before = chosen_device.get_pid_cpu(pid).total()
  for i in range(100):
    time.sleep(0.1)
    total_time_after = chosen_device.get_total_cpu().total()
    total_jiffy_after = chosen_device.get_pid_cpu(pid).total()
    cpu_usage = 100 * ((total_jiffy_after - total_jiffy_before)/(total_time_after - total_time_before))
    elapsed_cpu_usage.append(cpu_usage)
  
  print(f"elapsed_cpu_usage: {elapsed_cpu_usage}")





# if __name__ == "__main__":
#   devices = list_devices()
#   chosen_device = devices[0]

#   print(chosen_device.list_packages())