import os
import serial
import serial.tools.list_ports as serial_port
import platform


class BoardConn:
    def __init__(self, baud_rate):
        self._baud_rate = baud_rate
        self._platform_type = platform.platform()[0:5]
        
        _port_list = serial_port.comports()
        _get_port_ser = None
        if self._platform_type == 'macOS':
            _port_ser = '/dev/cu.usbmodem'
            for _port in _port_list:
                if _port.device[0:16] == _port_ser:
                    _get_port_ser = _port.device
                else:
                    pass
        else:
            _port_ser = '/dev/ttyACM'
            for _port in _port_list:
                if _port.device[0:11] == _port_ser:
                    _get_port_ser = _port.device
                else:
                    pass
            if _get_port_ser == None:
                os.system("sudo chmod a+rw {}".format(_get_port_ser))
            else:
                pass
        self._ard_ser = serial.Serial(_get_port_ser, self._baud_rate)
    
    def get_data_frame(self):
        return self._ard_ser.readline().decode()
    
    def get_data(self):
        _get_data = self._ard_ser.readline().decode()
        data = [0,0]
        try :
            if _get_data[0] == 'i':
                _sampletime  = _get_data[_get_data.index('a')+1:_get_data.index('b')]
                _aivalue = _get_data[_get_data.index('b')+1:_get_data.index('f')]
                data = [_sampletime, _aivalue]
            else:
                pass
        except:
            pass
        
        return data
    
    def close_ser(self):
        self._ard_ser.close()