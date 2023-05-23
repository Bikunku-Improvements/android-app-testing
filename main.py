import time
from ppadb.client import Client as AdbClient

testing_package = 'com.example.passenger_client'

client = AdbClient(host="127.0.0.1", port=5037)
HERTZ = 100

def list_devices():
  return client.devices()

def get_elapsed_cpu_usage(device):
  # I think this works?
  # Reference: https://stackoverflow.com/questions/1420426/how-to-calculate-the-cpu-usage-of-a-process-by-pid-in-linux-from-c/1424556#1424556
  elapsed_cpu_usage = []
  pid = device.get_pid(testing_package)
  total_time_before = device.get_total_cpu().total()
  total_jiffy_before = device.get_pid_cpu(pid).total()
  for i in range(100):
    time.sleep(0.1)
    total_time_after = device.get_total_cpu().total()
    total_jiffy_after = device.get_pid_cpu(pid).total()
    cpu_usage = 100 * ((total_jiffy_after - total_jiffy_before)/(total_time_after - total_time_before))
    elapsed_cpu_usage.append(cpu_usage)
  
  return elapsed_cpu_usage

if __name__ == "__main__":
  # make sure that the first element of the array is the device that we're testing
  devices = list_devices()
  chosen_device = devices[0]

  elapsed_cpu_usage = get_elapsed_cpu_usage()
  print(elapsed_cpu_usage)