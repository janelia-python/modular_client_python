python_arduino_device
=====================

This Python package creates a class named ArduinoDevice, which
contains an instance of serial_device2.SerialDevice and adds methods
to it, like auto discovery of available Arduinos in Linux, Windows,
and Mac OS X. This class automatically creates methods from available
functions reported by the Arduino when it is running the appropriate
firmware.

Authors::

    Peter Polidoro <polidorop@janelia.hhmi.org>

License::

    BSD

Example Usage::

    from arduino_device import ArduinoDevice
    dev = ArduinoDevice()
    dev = ArduinoDevice() # Automatically finds device if one available
    dev = ArduinoDevice('/dev/ttyACM0') # Linux
    dev = ArduinoDevice('/dev/tty.usbmodem262471') # Mac OS X
    dev = ArduinoDevice('COM3') # Windows
    dev.get_commands()
    devs = ArduinoDevices()  # Automatically finds all available devices
    devs.get_devices_info()
    dev = devs[0]

