python_arduino_device
=====================

This Python package (arduino\_device) creates a class named
ArduinoDevice, which contains an instance of
serial\_device2.SerialDevice and adds methods to it, like auto
discovery of available Arduinos in Linux, Windows, and Mac OS X. This
class automatically creates methods from available functions reported
by the Arduino when it is running the appropriate firmware.

Authors:

    Peter Polidoro <polidorop@janelia.hhmi.org>

License:

    BSD

##Example Usage


```python
from arduino_device import ArduinoDevice
dev = ArduinoDevice() # Automatically finds device if one available
dev = ArduinoDevice('/dev/ttyACM0') # Linux
dev = ArduinoDevice('/dev/tty.usbmodem262471') # Mac OS X
dev = ArduinoDevice('COM3') # Windows
dev.get_commands()
devs = ArduinoDevices()  # Automatically finds all available devices
devs.get_devices_info()
dev = devs[0]
```

##Installation

###Linux and Mac OS X

[Setup Python for Linux](./PYTHON_SETUP_LINUX.md)

[Setup Python for Mac OS X](./PYTHON_SETUP_MAC_OS_X.md)

```shell
mkdir -p ~/virtualenvs/arduino_device
virtualenv ~/virtualenvs/arduino_device
source ~/virtualenvs/arduino_device/bin/activate
pip install arduino_device
```

###Windows

[Setup Python for Windows](./PYTHON_SETUP_WINDOWS.md)

```shell
virtualenv C:\virtualenvs\arduino_device
C:\virtualenvs\arduino_device\Scripts\activate
pip install arduino_device
```
