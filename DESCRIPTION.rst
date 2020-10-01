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

    Peter Polidoro <peterpolidoro@gmail.com>

License::

    BSD

Example Usage::

    from modular_client import ModularClient
    dev = ModularClient()
    # Will try to automatically find device if one available. This may be slow if it
    # needs to search many serial ports. If it is not found automatically or to
    # speed up, specify port directly.
    dev = ModularClient(port='/dev/ttyACM0') # Linux specific port
    dev = ModularClient(port='/dev/tty.usbmodem262471') # Mac OS X specific port
    dev = ModularClient(port='COM3') # Windows specific port
    dev.get_device_id()
    dev.get_methods()
    from modular_client import ModularClients
    devs = ModularClients()
    # Will try to automatically find all available devices. This may be slow if it
    # needs to search many serial ports. If they are not found automatically or to
    # speed up, specify ports to use.
    devs = ModularClients(use_ports=['/dev/ttyACM0','/dev/ttyACM1']) # Linux
    devs = ModularClients(use_ports='(/dev/ttyACM)[0-1]') # Linux string RE alternative
    devs = ModularClients(use_ports=['/dev/tty.usbmodem262471','/dev/tty.usbmodem262472']) # Mac OS X
    devs = ModularClients(use_ports='(/dev/tty\.usbmodem26247)[1-2]') # Mac OS X RE Alternative
    devs = ModularClients(use_ports=['COM3','COM4']) # Windows
    devs = ModularClients(use_ports='(COM)[3-4]') # Windows RE Alternative
    devs.items()
    # dev = devs[name][form_factor][serial_number]
    devs = ModularClients(use_ports='(/dev/ttyACM)[0-1]',keys=[0,1])
    dev = devs[0]
    devs = ModularClients(use_ports='(/dev/ttyACM)[0-1]',keys='(device)[0-1]')
    dev = devs['device0']
    devs = ModularClients(use_ports='(/dev/ttyACM)[0-1]',ports_as_keys=True)
    dev = devs['/dev/ttyACM0']
