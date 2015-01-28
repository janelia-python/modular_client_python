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
    dev = ModularDevice()
    dev = ModularDevice() # Automatically finds device if one available
    dev = ModularDevice('/dev/ttyACM0') # Linux specific port
    dev = ModularDevice('/dev/tty.usbmodem262471') # Mac OS X specific port
    dev = ModularDevice('COM3') # Windows specific port
    dev.get_device_info()
    dev.get_methods()
    devs = ModularDevices()  # Automatically finds all available devices
    devs.items()
    dev = devs[name][serial_number]

