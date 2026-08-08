from machine import ADC
import time

force1 = ADC(27)
force2 = ADC(28)

while True:
    print(
        "Force 1:", force1.read_u16(),
        "Force 2:", force2.read_u16()
    )

    time.sleep(0.2)