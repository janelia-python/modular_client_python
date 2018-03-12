modular_client_python
=====================

This Python package creates a class named ModularClient, which
contains an instance of serial_interface.SerialInterface and adds methods
to it, like auto discovery of available modular devices in Linux,
Windows, and Mac OS X. This class automatically creates methods from
available functions reported by the modular device when it is running
the appropriate firmware. This is the modular device client library
for communicating with and calling remote methods on modular device
servers.

Authors::

    Peter Polidoro <polidorop@janelia.hhmi.org>

License::

    BSD

Example Usage::

    from modular_client import ModularClient
    dev = ModularClient() # Might automatically find device if one available
    # if it is not found automatically, specify port directly
    dev = ModularClient(port='/dev/ttyACM0') # Linux specific port
    dev = ModularClient(port='/dev/tty.usbmodem262471') # Mac OS X specific port
    dev = ModularClient(port='COM3') # Windows specific port
    dev.get_device_id()
    dev.get_methods()
    from modular_client import ModularClients
    devs = ModularClients()  # Might automatically find all available devices
    # if they are not found automatically, specify ports to use
    devs = ModularClients(use_ports=['/dev/ttyUSB0','/dev/ttyUSB1']) # Linux
    devs = ModularClients(use_ports=['/dev/tty.usbmodem262471','/dev/tty.usbmodem262472']) # Mac OS X
    devs = ModularClients(use_ports=['COM3','COM4']) # Windows
    devs.items()
    dev = devs[name][form_factor][serial_number]
