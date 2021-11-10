from ubinascii import hexlify
import machine
import time
import binascii
from machine import SoftI2C, I2C
import ctypes
sda=machine.Pin(4)
scl=machine.Pin(5)
i2c = I2C(0,sda=sda,scl=scl, freq=400000)

PWR_MODE = const(0x3E)
OPR_MODE = 0X3D
UNIT_SEL = 0X3B
PAGE_ID  = 0X07

ACC_X = 0x08
ACC_Y = 0x0A
ACC_Z = 0x0C
HEAD = 0x1A


def write_imu(device, register, data):
    buf = bytearray()
    buf.append(data)
    i2c.writeto_mem(device, register, buf)

def read_imu(device, register):
    try:
        data = i2c.readfrom_mem(device[0], register, 2)
        value = int.from_bytes(data, "little")
        if(value <= 32768):
            print("ACCELERATION: ", float(value) / 16, "\n")
        else:
            buf = bytearray()
            buf.append(~data[1])
            buf.append(~data[0])
            value = float(-(int.from_bytes(buf, 'big') + 1)) / 16
    except OSError:
        None    
    return value

def main():
    device = i2c.scan()
    write_imu(device[0], PWR_MODE, 0x00)
    write_imu(device[0], OPR_MODE, 0x00)
    write_imu(device[0], UNIT_SEL, 0x00)
    write_imu(device[0], OPR_MODE, 0x0C)
    
    print("OPMODE: ", int.from_bytes(i2c.readfrom_mem(device[0], 0x3D, 1), "little"))
    time.sleep(2)

    while True:
        try:
            try:
                data = i2c.readfrom_mem(device[0], HEAD, 2)
                value = int.from_bytes(data, "little")
                if(value <= 32768):
                    print("ACCELERATION: ", float(value) / 100, "\n")
                else:
                    buf = bytearray()
                    buf.append(~data[1])
                    buf.append(~data[0])
                    value = float(-(int.from_bytes(buf, 'big') + 1)) / 100
                    print("ACCELERATION: ", value , " \n\n")
            except OSError:
                None        
            time.sleep_ms(20)
        except KeyboardInterrupt:
            break

main()


