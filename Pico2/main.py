from machine import UART, Pin
import time

uart = UART(
    0,
    baudrate=9600,
    tx=Pin(0)
)

while True:
    uart.write("Hello\n")
    time.sleep(1)