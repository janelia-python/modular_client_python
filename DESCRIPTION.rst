python_remote_device
=====================

This Python package creates a class named RemoteDevice, which contains
an instance of serial_device2.SerialDevice and adds methods to it,
like auto discovery of available remote devices in Linux, Windows, and
Mac OS X. This class automatically creates methods from available
functions reported by the remote device when it is running the
appropriate firmware.

Authors::

    Peter Polidoro <polidorop@janelia.hhmi.org>

License::

    BSD

Example Usage::

    from remote_device import RemoteDevice
    dev = RemoteDevice()
    dev = RemoteDevice() # Automatically finds device if one available
    dev = RemoteDevice('/dev/ttyACM0') # Linux specific port
    dev = RemoteDevice('/dev/tty.usbmodem262471') # Mac OS X specific port
    dev = RemoteDevice('COM3') # Windows specific port
    dev.get_device_info()
    dev.get_methods()
    devs = RemoteDevices()  # Automatically finds all available devices
    devs.items()
    dev = devs[name][serial_number]

