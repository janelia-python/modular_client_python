#modular_device_python

This Python package (modular\_device) creates a class named
ModularDevice, which contains an instance of
serial\_device2.SerialDevice and adds methods to it, like auto
discovery of available modular devices in Linux, Windows, and Mac OS
X. This class automatically creates methods from available functions
reported by the modular device when it is running the appropriate
firmware.

Authors:

    Peter Polidoro <polidorop@janelia.hhmi.org>

License:

    BSD

##Example Usage


```python
from modular_device import ModularDevice
dev = ModularDevice() # Might automatically finds device if one available
# if it is not found automatically, specify port directly
dev = ModularDevice(port='/dev/ttyACM0') # Linux specific port
dev = ModularDevice(port='/dev/tty.usbmodem262471') # Mac OS X specific port
dev = ModularDevice(port='COM3') # Windows specific port
dev.get_device_info()
dev.get_methods()
```

```python
from modular_device import ModularDevices
devs = ModularDevices()  # Might automatically find all available devices
# if they are not found automatically, specify ports to use
devs = ModularDevices(use_ports=['/dev/ttyUSB0','/dev/ttyUSB1']) # Linux
devs = ModularDevices(use_ports=['/dev/tty.usbmodem262471','/dev/tty.usbmodem262472']) # Mac OS X
devs = ModularDevices(use_ports=['COM3','COM4']) # Windows
devs.items()
dev = devs[name][serial_number]
```

##More Detailed Modular Device Information

<https://github.com/janelia-modular-devices/modular-devices>

##Installation

[Setup Python](https://github.com/janelia-pypi/python_setup)

###Install Latest Version of Arduino on your Host Machine

<http://arduino.cc/en/Guide/HomePage>

On linux, you may need to add yourself to the group 'dialout' in order
to have write permissions on the USB port:

```shell
sudo usermod -aG dialout $USER
sudo reboot
```

###Linux and Mac OS X

```shell
mkdir -p ~/virtualenvs/modular_device
virtualenv ~/virtualenvs/modular_device
source ~/virtualenvs/modular_device/bin/activate
pip install modular_device
```

###Windows

```shell
virtualenv C:\virtualenvs\modular_device
C:\virtualenvs\modular_device\Scripts\activate
pip install modular_device
```
