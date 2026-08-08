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
force = ADC(27)

buttons = [
    Pin(3, Pin.IN, Pin.PULL_UP),
    Pin(4, Pin.IN, Pin.PULL_UP),
    Pin(5, Pin.IN, Pin.PULL_UP),
    Pin(6, Pin.IN, Pin.PULL_UP),
    Pin(7, Pin.IN, Pin.PULL_UP),
    Pin(8, Pin.IN, Pin.PULL_UP),
    Pin(10, Pin.IN, Pin.PULL_UP)
]

sine_switch = Pin(11, Pin.IN, Pin.PULL_UP)
square_switch = Pin(12, Pin.IN, Pin.PULL_UP)
saw_switch = Pin(13, Pin.IN, Pin.PULL_UP)

frequencies = [
    262,
    294,
    330,
    349,
    392,
    440,
    494
]

phase = 0
vibrato_phase = 0

while True:

    volume = (potent.read_u16() * 15000) // 65535

    pressure = force.read_u16()

    if pressure < 20000:
        vibrato_depth = 0
    else:
        vibrato_depth = ((pressure - 20000) * 8) // 45535

    frequency = 0

    for i in range(7):
        if buttons[i].value() == 0:
            frequency = frequencies[i]
            break

    if square_switch.value() == 1:
        sound = 2

    elif saw_switch.value() == 1:
        sound = 3

    else:
        sound = 1

    vibrato = vibrato_depth * math.sin(vibrato_phase)
    current_frequency = frequency + vibrato

    vibrato_phase += 2 * math.pi * 5 * chunk_size / sample_rate

    if vibrato_phase >= 2 * math.pi:
        vibrato_phase -= 2 * math.pi

    samples = bytearray()

    for i in range(chunk_size):

        if frequency > 0:

            if sound == 1:
                wave = math.sin(phase)

            elif sound == 2:
                if phase < math.pi:
                    wave = 1
                else:
                    wave = -1

            else:
                wave = (phase / math.pi) - 1

            value = int(volume * wave)

            phase += 2 * math.pi * current_frequency / sample_rate

            if phase >= 2 * math.pi:
                phase -= 2 * math.pi

        else:
            value = 0

        samples += struct.pack("<h", value)

    audio.write(samples)