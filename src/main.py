from ppadb.client import Client as AdbClient
from ppadb.device import Device

import time

from perf import Perf

"""
User defined parameters, you can modify these
"""
TESTING_PACKAGE = 'com.android.chrome'  # package that we are testing
SECONDS = 25  # length of the test in seconds

"""
Do not modify these
"""
CONNECTED_ADB_CLIENT = AdbClient(host="127.0.0.1", port=5037)
CONNECTED_DEVICE: Device = CONNECTED_ADB_CLIENT.devices()[0]

if __name__ == "__main__":
    p = Perf(CONNECTED_DEVICE, TESTING_PACKAGE)
    p.start()

    try:
        time.sleep(500)
    except KeyboardInterrupt:
        p.stop()
        p.csv2images()
