from ppadb.client import Client as AdbClient
from ppadb.device import Device

"""
User defined parameters, you can modify these
"""
TESTING_PACKAGE = 'com.example.passenger_client'  # package that we are testing
SECONDS = 25  # length of the test in seconds

"""
Do not modify these
"""
CONNECTED_ADB_CLIENT = AdbClient(host="127.0.0.1", port=5037)
CONNECTED_DEVICE = CONNECTED_ADB_CLIENT.devices()[0]

if __name__ == "__main__":
    pass
