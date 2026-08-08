from machine import I2S, Pin, ADC
import math
import struct

sample_rate = 8000
chunk_size = 64

audio = I2S(
    0,
    sck=Pin(1),
    ws=Pin(2),
    sd=Pin(0),
    mode=I2S.TX,
    bits=16,
    format=I2S.MONO,
    rate=sample_rate,
    ibuf=8000
)

potent = ADC(26)

button1 = Pin(3, Pin.IN, Pin.PULL_UP)
button2 = Pin(4, Pin.IN, Pin.PULL_UP)
button3 = Pin(5, Pin.IN, Pin.PULL_UP)
button4 = Pin(6, Pin.IN, Pin.PULL_UP)
button5 = Pin(7, Pin.IN, Pin.PULL_UP)
button6 = Pin(8, Pin.IN, Pin.PULL_UP)
button7 = Pin(10, Pin.IN, Pin.PULL_UP)

sine_switch = Pin(11, Pin.IN, Pin.PULL_UP)
square_switch = Pin(12, Pin.IN, Pin.PULL_UP)
saw_switch = Pin(13, Pin.IN, Pin.PULL_UP)

buttons = [
    button1,
    button2,
    button3,
    button4,
    button5,
    button6,
    button7
]

frequencies = [
    262,
    294,
    330,
    349,
    392,
    440,
    494
]

sine_table = []

for i in range(256):
    sine_table.append(
        math.sin(2 * math.pi * i / 256)
    )

phases = [0] * 7

steps = []

for frequency in frequencies:
    steps.append(
        int(frequency * 65536 / sample_rate)
    )

samples = bytearray(chunk_size * 2)

while True:

    volume = (potent.read_u16() * 15000) // 65535

    active = []

    for i in range(7):
        if buttons[i].value() == 0:
            active.append(i)

    if sine_switch.value() == 1:
        sound = 1

    elif square_switch.value() == 1:
        sound = 2

    elif saw_switch.value() == 1:
        sound = 3

    else:
        sound = 1

    for sample in range(chunk_size):

        value = 0

        for i in active:

            position = phases[i] >> 8

            if sound == 1:
                wave = sine_table[position]

            elif sound == 2:
                if position < 128:
                    wave = 1
                else:
                    wave = -1

            else:
                wave = (position / 128) - 1

            value += wave

            phases[i] = (phases[i] + steps[i]) & 65535

        if len(active) > 0:
            value = int(value * volume / len(active))
        else:
            value = 0

        struct.pack_into(
            "<h",
            samples,
            sample * 2,
            value
        )

    audio.write(samples)