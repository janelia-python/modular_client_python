'''
This Python package (remote_device) creates a class named RemoteDevice,
which contains an instance of serial_device2.SerialDevice and adds
methods to it, like auto discovery of available remote devices in Linux,
Windows, and Mac OS X. This class automatically creates methods from
available functions reported by the remote device when it is running the
appropriate firmware.
'''
from remote_device import RemoteDevice, RemoteDevices, find_remote_device_ports, find_remote_device_port, __version__
