'''
This Python package (modular_client) creates a class named ModularClient,
which contains an instance of serial_device2.SerialDevice and adds
methods to it, like auto discovery of available modular devices in Linux,
Windows, and Mac OS X. This class automatically creates methods from
available functions reported by the modular device when it is running the
appropriate firmware.
'''
from .modular_client import ModularClient, ModularClients, find_modular_device_ports, find_modular_device_port, __version__
