from machine import I2S, Pin, ADC
import math
import struct

sample_rate = 8000

audio = I2S(
    0,
    sck=Pin(1),
    ws=Pin(2),
    sd=Pin(0),
    mode=I2S.TX,
    bits=16,
    format=I2S.MONO,
    rate=sample_rate,
    ibuf=4000
)

potent = ADC(26)

button1 = Pin(3, Pin.IN, Pin.PULL_UP)
button2 = Pin(4, Pin.IN, Pin.PULL_UP)
button3 = Pin(5, Pin.IN, Pin.PULL_UP)
button4 = Pin(6, Pin.IN, Pin.PULL_UP)
button5 = Pin(7, Pin.IN, Pin.PULL_UP)
button6 = Pin(8, Pin.IN, Pin.PULL_UP)
button7 = Pin(10, Pin.IN, Pin.PULL_UP)

buttons = [
    (button1, 262),
    (button2, 294),
    (button3, 330),
    (button4, 349),
    (button5, 392),
    (button6, 440),
    (button7, 494)
]

phase = 0

while True:

    volume = (potent.read_u16() * 15000) // 65535

    frequency = 0

    for button, note in buttons:
        if button.value() == 0:
            frequency = note
            break

    samples = bytearray()

    for i in range(400):

        if frequency > 0:
            value = int(volume * math.sin(phase))

            phase += 2 * math.pi * frequency / sample_rate

            if phase >= 2 * math.pi:
                phase -= 2 * math.pi

        else:
            value = 0

        samples += struct.pack("<h", value)

    audio.write(samples)