from machine import ADC
import time

force = ADC(27)

while True:
    print(force.read_u16())
    time.sleep(0.1)