modular_device_python
=====================

This Python package creates a class named ModularDevice, which contains
an instance of serial_device2.SerialDevice and adds methods to it,
like auto discovery of available modular devices in Linux, Windows, and
Mac OS X. This class automatically creates methods from available
functions reported by the modular device when it is running the
appropriate firmware.

Authors::

    Peter Polidoro <polidorop@janelia.hhmi.org>

License::

    BSD

Example Usage::

    from modular_device import ModularDevice
    dev = ModularDevice() # Might automatically finds device if one available
    # if it is not found automatically, specify port directly
    dev = ModularDevice(port='/dev/ttyACM0') # Linux specific port
    dev = ModularDevice(port='/dev/tty.usbmodem262471') # Mac OS X specific port
    dev = ModularDevice(port='COM3') # Windows specific port
    dev.get_device_info()
    dev.get_methods()
    from modular_device import ModularDevices
    devs = ModularDevices()  # Might automatically find all available devices
    # if they are not found automatically, specify ports to try
    devs = ModularDevices(try_ports=['/dev/ttyUSB0','/dev/ttyUSB1']) # Linux
    devs = ModularDevices(try_ports=['/dev/tty.usbmodem262471','/dev/tty.usbmodem262472']) # Mac OS X
    devs = ModularDevices(try_ports=['COM3','COM4']) # Windows
    devs.items()
    dev = devs[name][serial_number]

