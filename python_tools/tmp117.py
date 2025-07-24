import pyftdi.serialext
import binascii
import time

class bcolors:
    OK = '\033[92m'
    INFO = '\033[94m'
    WARNING = '\033[33m'
    ERROR = '\033[31m'
    ENDC = '\033[0m'

class tmp117:
    #def __init__(self, url='ftdi://ftdi:232:AK05MCQN/1', writeFile=False):
    # url='/dev/ttyUSB#' #==0 => Tiancheng's PCB und #==1 => Tile Lab board #==2 => Sensor on six matrix setup
    def __init__(self, url='/dev/ttyUSB0', writeFile=False):
        self._url = url
        self._delay = 0.05
        self._timeout = 2
        # Initialize I2C (COM port via ftdi232rl)
        self._serialPort = pyftdi.serialext.serial_for_url(url=self._url, baudrate=19200, bytesize=8, timeout=self._timeout)
        # Register addresses
        self._reg_temp = 0x00
        self._sensor_addr = []
        self.detectSensors()

    def re_init(self):
        self._serialPort.close()
        self._serialPort = pyftdi.serialext.serial_for_url(url=self._url, baudrate=19200, bytesize=8, timeout=self._timeout)

    def detectSensors(self):
        print(f"{bcolors.INFO}Detecting sensors!{bcolors.ENDC}")
        for device in range(72, 75):
            try:
                packet = self._prepare_sq(address=device, r_w=1)  # TODO
                r1 = self._serialPort.write(packet)
                time.sleep(self._delay)
                read_back = self._serialPort.read_all()
                time.sleep(self._delay)
                if (read_back != b'\xff\xff') and (read_back != b''):
                    print(hex(device), bcolors.OK + "GOOD" + bcolors.ENDC, "read back: ", int.from_bytes(read_back, byteorder='big') * 0.0078125)
                    self._sensor_addr.append(device)
            except Exception as e:  # Catch the exception and print error message
                print(device, bcolors.ERROR + "Cannot open device: " + str(device) + bcolors.ENDC, "Error:", str(e))

    def read_temp(self):
        if not self._sensor_addr:
            print(bcolors.WARNING + "No sensors detected!" + bcolors.ENDC)
            return []
        
        temp_c = []
        for address in self._sensor_addr:
            packet = self._prepare_sq(address=address, r_w=1)  # TODO
            res = self._read_ftdi(packet)
            #print('address: ', hex(address), ' => ', res)
            temp_c.append(res)
        return temp_c

    def _prepare_sq(self, address, r_w):
        addr_full = ((address & 0xff) << 1) + r_w
        packet = bytearray()
        packet.append(0x55)
        packet.append(addr_full)
        packet.append(self._reg_temp)
        packet.append(0x02)  # Number of bytes to read back
        return packet

    def close_port(self):
        self._serialPort.close()

    def _read_ftdi(self, packet):
        time.sleep(self._delay)
        r1 = self._serialPort.write(packet)
        time.sleep(self._delay)
        data = self._serialPort.read_all()
        #print("Data: ", data)
        res = int.from_bytes(data, byteorder='big', signed=True) * 0.0078125
        return round(res, 2)

    def get_address(self):
        return self._sensor_addr
