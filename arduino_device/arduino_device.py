import serial
import time
import atexit
import json
import functools
import operator
import platform
import os
import inflection

from serial_interface import SerialInterface, SerialInterfaces, find_serial_interface_ports, WriteFrequencyError

try:
    from pkg_resources import get_distribution, DistributionNotFound
    _dist = get_distribution('arduino_device')
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, 'arduino_device')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except (ImportError,DistributionNotFound):
    __version__ = None
else:
    __version__ = _dist.version

DEBUG = False
BAUDRATE = 9600

class ArduinoDevice(object):
    '''
    ArduinoDevice contains an instance of
    serial_interface.SerialInterface and adds methods to it, like auto
    discovery of available Arduinos in Linux, Windows, and Mac OS
    X. This class automatically creates methods from available functions
    reported by the Arduino when it is running the appropriate firmware.

    Example Usage:

    dev = ArduinoDevice() # Automatically finds device if one available
    dev = ArduinoDevice('/dev/ttyACM0') # Linux
    dev = ArduinoDevice('/dev/tty.usbmodem262471') # Mac OS X
    dev = ArduinoDevice('COM3') # Windows
    dev.get_commands()
    '''
    _TIMEOUT = 0.05
    _WRITE_WRITE_DELAY = 0.05
    _RESET_DELAY = 2.0
    _CMD_GET_DEVICE_INFO = 0
    _CMD_GET_COMMANDS = 1
    _CMD_GET_RESPONSE_CODES = 2

    def __init__(self,*args,**kwargs):
        model_number = None
        serial_number = None
        if 'debug' in kwargs:
            self.debug = kwargs['debug']
        else:
            kwargs.update({'debug': DEBUG})
            self.debug = DEBUG
        if 'try_ports' in kwargs:
            try_ports = kwargs.pop('try_ports')
        else:
            try_ports = None
        if 'baudrate' not in kwargs:
            kwargs.update({'baudrate': BAUDRATE})
        elif (kwargs['baudrate'] is None) or (str(kwargs['baudrate']).lower() == 'default'):
            kwargs.update({'baudrate': BAUDRATE})
        if 'timeout' not in kwargs:
            kwargs.update({'timeout': self._TIMEOUT})
        if 'write_write_delay' not in kwargs:
            kwargs.update({'write_write_delay': self._WRITE_WRITE_DELAY})
        if 'model_number' in kwargs:
            model_number = kwargs.pop('model_number')
        if 'serial_number' in kwargs:
            serial_number = kwargs.pop('serial_number')
        if ('port' not in kwargs) or (kwargs['port'] is None):
            port =  find_arduino_device_port(baudrate=kwargs['baudrate'],
                                             model_number=model_number,
                                             serial_number=serial_number,
                                             try_ports=try_ports,
                                             debug=kwargs['debug'])
            kwargs.update({'port': port})

        t_start = time.time()
        self._serial_interface = SerialInterface(*args,**kwargs)
        atexit.register(self._exit_arduino_device)
        time.sleep(self._RESET_DELAY)
        self._rsp_dict = None
        self._rsp_dict = self._get_rsp_dict()
        self._cmd_dict = self._get_cmd_dict()
        self._cmd_dict_inv = dict([(v,k) for (k,v) in self._cmd_dict.items()])
        self._create_cmds()
        self._get_device_info()
        t_end = time.time()
        self._debug_print('Initialization time =', (t_end - t_start))

    def _debug_print(self, *args):
        if self.debug:
            print(*args)

    def _exit_arduino_device(self):
        pass

    def _args_to_cmd_str(self,*args):
        cmd_list = ['[', ','.join(map(str,args)), ']']
        cmd_str = ''.join(cmd_list)
        cmd_str = cmd_str + '\n';
        return cmd_str

    def _send_cmd_get_rsp(self,*args):

        '''Sends Arduino command to device over serial port and
        returns response'''

        cmd_str = self._args_to_cmd_str(*args)
        self._debug_print('cmd_str', cmd_str)
        rsp_str = self._serial_interface.write_read(cmd_str,use_readline=True,check_write_freq=True)
        if rsp_str is None:
            rsp_dict = {}
            return rsp_dict
        self._debug_print('rsp_str', rsp_str)
        try:
            rsp_dict = json_str_to_dict(rsp_str)
        except Exception as e:
            err_msg = 'Unable to parse device response {0}.'.format(str(e))
            raise IOError(err_msg)
        try:
            status = rsp_dict.pop('status')
        except KeyError:
            err_msg = 'Device response does not contain status.'
            raise IOError(err_msg)
        try:
            rsp_cmd_id  = rsp_dict.pop('cmd_id')
        except KeyError:
            err_msg = 'Device response does not contain cmd_id.'
            raise IOError(err_msg)
        if not rsp_cmd_id == args[0]:
            raise IOError('Device response cmd_id does not match that sent.')
        if self._rsp_dict is not None:
            if status == self._rsp_dict['rsp_error']:
                try:
                    dev_err_msg = '(from device) {0}'.format(rsp_dict['err_msg'])
                except KeyError:
                    dev_err_msg = "Error message missing."
                err_msg = '{0}'.format(dev_err_msg)
                raise IOError(err_msg)
        return rsp_dict

    def _get_device_info(self):
        self.device_info = self._send_cmd_get_rsp(self._CMD_GET_DEVICE_INFO)
        try:
            self.model_number = self.device_info['model_number']
        except KeyError:
            self.model_number = None
        try:
            self.serial_number = self.device_info['serial_number']
        except KeyError:
            self.serial_number = None

    def _get_cmd_dict(self):
        cmd_dict = self._send_cmd_get_rsp(self._CMD_GET_COMMANDS)
        return cmd_dict

    def _get_rsp_dict(self):
        rsp_dict = self._send_cmd_get_rsp(self._CMD_GET_RESPONSE_CODES)
        check_dict_for_key(rsp_dict,'rsp_success',dname='rsp_dict')
        check_dict_for_key(rsp_dict,'rsp_error',dname='rsp_dict')
        return rsp_dict

    def _send_cmd_by_name(self,name,*args):
        cmd_id = self._cmd_dict[name]
        cmd_args = [cmd_id]
        cmd_args.extend(args)
        rsp = self._send_cmd_get_rsp(*cmd_args)
        return rsp

    def _send_all_cmds(self):
        print('\nSend All Commands')
        print('-------------------')
        for cmd_id, cmd_name in sorted(self._cmd_dict_inv.items()):
            print('cmd: {0}, {1}'.format(cmd_name,cmd_id))
            rsp = self._send_cmd_get_rsp(cmd_id)
            print('rsp: {0}'.format(rsp))
            print()
        print()

    def _cmd_func_base(self,cmd_name,*args):
        if len(args) == 1 and type(args[0]) is dict:
            args_dict = args[0]
            args_list = self._args_dict_to_list(args_dict)
        else:
            args_list = args
        rsp_dict = self._send_cmd_by_name(cmd_name,*args_list)
        if rsp_dict:
            ret_value = self._process_rsp_dict(rsp_dict)
            return ret_value

    def _create_cmds(self):
        self._cmd_func_dict = {}
        for cmd_id, cmd_name in sorted(self._cmd_dict_inv.items()):
            cmd_func = functools.partial(self._cmd_func_base, cmd_name)
            setattr(self,inflection.underscore(cmd_name),cmd_func)
            self._cmd_func_dict[cmd_name] = cmd_func

    def _process_rsp_dict(self,rsp_dict):
        if len(rsp_dict) == 1:
            ret_value = list(rsp_dict.values())[0]
        else:
            all_values_empty = True
            for v in list(rsp_dict.values()):
                if not type(v) == str or v:
                    all_values_empty = False
                    break
            if all_values_empty:
                ret_value = sorted(rsp_dict.keys())
            else:
                ret_value = rsp_dict
        return ret_value

    def _args_dict_to_list(self,args_dict):
        key_set = set(args_dict.keys())
        order_list = sorted([(num,name) for (name,num) in order_dict.items()])
        args_list = [args_dict[name] for (num, name) in order_list]
        return args_list

    def close(self):
        '''
        Close the device serial port.
        '''
        self._serial_interface.close()

    def get_port(self):
        return self._serial_interface.port

    def get_commands(self):
        '''
        Get a list of Arduino commands automatically attached as class methods.
        '''
        return [inflection.underscore(key) for key in list(self._cmd_dict.keys())]


class ArduinoDevices(list):
    '''
    ArduinoDevices inherits from list and automatically populates it
    with ArduinoDevices on all available serial ports.

    Example Usage:

    devs = ArduinoDevices()  # Automatically finds all available devices
    devs.get_devices_info()
    dev = devs[0]
    '''
    def __init__(self,*args,**kwargs):
        if ('use_ports' not in kwargs) or (kwargs['use_ports'] is None):
            arduino_device_ports = find_arduino_device_ports(*args,**kwargs)
        else:
            arduino_device_ports = use_ports

        for port in arduino_device_ports:
            kwargs.update({'port': port})
            self.append_device(*args,**kwargs)

        self.sort_by_model_number()

    def append_device(self,*args,**kwargs):
        self.append(ArduinoDevice(*args,**kwargs))

    def get_devices_info(self):
        arduino_devices_info = []
        for dev in self:
            arduino_devices_info.append(dev.device_info)
        return arduino_devices_info

    def sort_by_model_number(self,*args,**kwargs):
        kwargs['key'] = operator.attrgetter('model_number','serial_number')
        self.sort(**kwargs)

    def get_by_model_number(self,model_number):
        dev_list = []
        for device_index in range(len(self)):
            dev = self[device_index]
            if dev.model_number == model_number:
                dev_list.append(dev)
        if len(dev_list) == 1:
            return dev_list[0]
        elif 1 < len(dev_list):
            return dev_list

    def sort_by_serial_number(self,*args,**kwargs):
        self.sort_by_model_number(*args,**kwargs)

    def get_by_serial_number(self,serial_number):
        dev_list = []
        for device_index in range(len(self)):
            dev = self[device_index]
            if dev.serial_number == serial_number:
                dev_list.append(dev)
        if len(dev_list) == 1:
            return dev_list[0]
        elif 1 < len(dev_list):
            return dev_list


def check_dict_for_key(d,k,dname=''):
    if not k in d:
        if not dname:
            dname = 'dictionary'
        raise IOError('{0} does not contain {1}'.format(dname,k))

def json_str_to_dict(json_str):
    json_dict =  json.loads(json_str,object_hook=json_decode_dict)
    return json_dict

def json_decode_dict(data):
    """
    Object hook for decoding dictionaries from serialized json data. Ensures that
    all strings are unpacked as str objects rather than unicode.
    """
    rv = {}
    for key, value in data.items():
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(value, str):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = json_decode_list(value)
        elif isinstance(value, dict):
            value = json_decode_dict(value)
        rv[key] = value
    return rv

def json_decode_list(data):
    """
    Object hook for decoding lists from serialized json data. Ensures that
    all strings are unpacked as str objects rather than unicode.
    """
    rv = []
    for item in data:
        if isinstance(item, str):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = json_decode_list(item)
        elif isinstance(item, dict):
            item = json_decode_dict(item)
        rv.append(item)
    return rv

def find_arduino_device_ports(baudrate=None, model_number=None, serial_number=None, try_ports=None, debug=DEBUG):
    serial_interface_ports = find_serial_interface_ports(try_ports=try_ports, debug=debug)
    os_type = platform.system()
    if os_type == 'Darwin':
        serial_interface_ports = [x for x in serial_interface_ports if 'tty.usbmodem' in x or 'tty.usbserial' in x]

    if type(model_number) is int:
        model_number = [model_number]
    if type(serial_number) is int:
        serial_number = [serial_number]

    arduino_device_ports = {}
    for port in serial_interface_ports:
        try:
            dev = ArduinoDevice(port=port,baudrate=baudrate,debug=debug)
            if ((model_number is None ) and (dev.model_number is not None)) or (dev.model_number in model_number):
                if ((serial_number is None) and (dev.serial_number is not None)) or (dev.serial_number in serial_number):
                    arduino_device_ports[port] = {'model_number': dev.model_number,
                                                  'serial_number': dev.serial_number}
            dev.close()
        except (serial.SerialException, IOError):
            pass
    return arduino_device_ports

def find_arduino_device_port(baudrate=None, model_number=None, serial_number=None, try_ports=None, debug=DEBUG):
    arduino_device_ports = find_arduino_device_ports(baudrate=baudrate,
                                                     model_number=model_number,
                                                     serial_number=serial_number,
                                                     try_ports=try_ports,
                                                     debug=debug)
    if len(arduino_device_ports) == 1:
        return list(arduino_device_ports.keys())[0]
    elif len(arduino_device_ports) == 0:
        serial_interface_ports = find_serial_interface_ports(try_ports)
        err_str = 'Could not find any Arduino devices. Check connections and permissions.\n'
        err_str += 'Tried ports: ' + str(serial_interface_ports)
        raise RuntimeError(err_str)
    else:
        err_str = 'Found more than one Arduino device. Specify port or model_number and/or serial_number.\n'
        err_str += 'Matching ports: ' + str(arduino_device_ports)
        raise RuntimeError(err_str)


# -----------------------------------------------------------------------------------------
if __name__ == '__main__':

    debug = False
    dev = ArduinoDevice(debug=debug)
