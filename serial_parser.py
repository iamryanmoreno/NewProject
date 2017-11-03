import serial
from base import Base
import time


class SerialParser(Base):

    ser = None
    timeout = 5

    def __init__(self, port='/dev/ttyUSB0', baudrate=1200, timeout=5):
    #def __init__(self, port='COM9', baudrate=1200, timeout=5):
        Base.__init__(self)
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.timeout = timeout

    def read_data(self):
        """
        Read data from serial line until carriage return.
        :return:
        """
        line = ''
        s_time = time.time()
        while True:
            if time.time() - s_time >= self.timeout:
                break
            else:
                try:
                    data = self.ser.read()
                    if data == '\r':
                        break
                    else:
                        line = line + data
                except serial.SerialException as e:
                    print "Error, ", e
                except OSError as e:
                    print "OS Error, ", e

        return line.strip()

