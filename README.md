python_arduino_device
=====================

This Python package (arduino\_device) creates a class named
ArduinoDevice, which contains an instance of
serial\_interface.SerialInterface and adds methods to it, like auto
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

```shell
mkdir ~/venvs/
cd ~/venvs/
python3 -m venv arduino_device
source ~/venvs/arduino_device/bin/activate
pip install arduino_device
```

###Windows

```shell
python3 -m venv C:\venvs\arduino_device
C:\venvs\arduino_device\Scripts\activate
pip install arduino_device
```
