from machine import UART
import machine
import time

uart = UART(0, 9600,tx=machine.Pin(0),rx=machine.Pin(1))

while True:
    try:
        data = uart.readline()
        if(data != 0):
            print("Data found\n")
            print(data)
        else:
            print("No Data\n")
    except KeyboardInterrupt:
        break
    time.sleep(100)
