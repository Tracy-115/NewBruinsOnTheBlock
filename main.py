from machine import Pin
import time

sine_switch = Pin(11, Pin.IN, Pin.PULL_UP)
square_switch = Pin(12, Pin.IN, Pin.PULL_UP)
saw_switch = Pin(13, Pin.IN, Pin.PULL_UP)

while True:
    print(
        sine_switch.value(),
        square_switch.value(),
        saw_switch.value()
    )
    time.sleep(0.2)