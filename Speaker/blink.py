from machine import UART, Pin
import time

uart = UART(
    0,
    baudrate=9600,
    rx=Pin(17)
)

while True:
    if uart.any():
        data = uart.readline()

        if data:
            print(data)

    time.sleep(0.01)