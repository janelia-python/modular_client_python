'''
This Python package (arduino_device) creates a class named
ArduinoDevice, which contains an instance of serial_device2.SerialDevice
and adds methods to it, like auto discovery of available Arduinos in
Linux, Windows, and Mac OS X. This class automatically creates methods
from available functions reported by the Arduino when it is running the
appropriate firmware.
'''
from .arduino_device import ArduinoDevice, ArduinoDevices, find_arduino_device_ports, find_arduino_device_port, __version__
