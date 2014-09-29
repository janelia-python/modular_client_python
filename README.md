python_arduino_device
=====================

This Python package (arduino\_device) creates a class named
ArduinoDevice, which contains an instance of
serial\_device2.SerialDevice and adds methods to it, like auto
discovery of available Arduinos in Linux, Windows, and Mac OS X. This
class automatically creates methods from available functions reported
by the Arduino when using the DeviceInterface Arduino library located
in the repository https://github.com/JaneliaSciComp/arduino-libraries

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
devs.sort_by_port()
dev = devs[0]
```

##Installation

###Linux and Mac OS X

```shell
mkdir -p ~/virtualenvs/arduino_device
virtualenv ~/virtualenvs/arduino_device
source ~/virtualenvs/arduino_device/bin/activate
pip install arduino_device
```

###Windows

Download Python 2.7.8 Windows Installer from:

    https://www.python.org/download

Add to path:

    C:\Python27\

Download get-pip.py from:

    https://bootstrap.pypa.io/get-pip.py

Run:

```shell
python get-pip.py
```

Add to path:

    C:\Python27\Scripts\

Run:

```shell
pip install virtualenv
mkdir C:\virtualenvs
virtualenv C:\virtualenvs\arduino_device
C:\virtualenvs\arduino_device\Scripts\activate
pip install https://github.com/JaneliaSciComp/python_arduino_device/zipball/master
```
