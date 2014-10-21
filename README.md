python_remote_device
=====================

This Python package (remote\_device) creates a class named
RemoteDevice, which contains an instance of
serial\_device2.SerialDevice and adds methods to it, like auto
discovery of available remote devices in Linux, Windows, and Mac OS
X. This class automatically creates methods from available functions
reported by the remote device when it is running the appropriate
firmware.

Authors:

    Peter Polidoro <polidorop@janelia.hhmi.org>

License:

    BSD

##Example Usage


```python
from remote_device import RemoteDevice
dev = RemoteDevice() # Automatically finds device if one available
dev = RemoteDevice('/dev/ttyACM0') # Linux
dev = RemoteDevice('/dev/tty.usbmodem262471') # Mac OS X
dev = RemoteDevice('COM3') # Windows
dev.get_methods()
devs = RemoteDevices()  # Automatically finds all available devices
devs.get_devices_info()
dev = devs[0]
```

More Detailed Examples:

<https://github.com/JaneliaSciComp/arduino_remote_device>

##Installation

###Linux and Mac OS X

[Setup Python for Linux](./PYTHON_SETUP_LINUX.md)

[Setup Python for Mac OS X](./PYTHON_SETUP_MAC_OS_X.md)

```shell
mkdir -p ~/virtualenvs/remote_device
virtualenv ~/virtualenvs/remote_device
source ~/virtualenvs/remote_device/bin/activate
pip install remote_device
```

###Windows

[Setup Python for Windows](./PYTHON_SETUP_WINDOWS.md)

```shell
virtualenv C:\virtualenvs\remote_device
C:\virtualenvs\remote_device\Scripts\activate
pip install remote_device
```
