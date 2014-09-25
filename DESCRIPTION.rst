python_arduino_device
=====================

This Python package creates a class named ArduinoDevice, which inherits
from SerialDevice and adds methods to it, like auto discovery of
available Arduinos in Linux, Windows, and Mac OS X.

Authors:
Peter Polidoro <polidorop@janelia.hhmi.org>

License:
BSD

Example Usage::

    from arduino_device import ArduinoDevice
    dev = ArduinoDevice()
    dev.get_arduino_device_info()
    dev.get_arduino_commands()

