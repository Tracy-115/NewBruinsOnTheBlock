from machine import I2S, Pin, ADC, I2C
import math
import struct
import time

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

i2c = I2C(
    0,
    sda=Pin(20),
    scl=Pin(21),
    freq=400000
)

MPU = 0x68

i2c.writeto_mem(
    MPU,
    0x6B,
    b"\x00"
)

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

octave = 4
tilted = False

last_imu_read = time.ticks_ms()


def read_accel_y():

    data = i2c.readfrom_mem(
        MPU,
        0x3D,
        2
    )

    value = (data[0] << 8) | data[1]

    if value > 32767:
        value -= 65536

    return value


while True:

    if time.ticks_diff(time.ticks_ms(), last_imu_read) > 100:

        y = read_accel_y()

        if not tilted:

            if y > 9000:

                octave += 1

                if octave > 8:
                    octave = 8

                tilted = True
                print("Octave:", octave)

            elif y < -9000:

                octave -= 1

                if octave < 1:
                    octave = 1

                tilted = True
                print("Octave:", octave)

        if -5000 < y < 5000:
            tilted = False

        last_imu_read = time.ticks_ms()

    volume = (potent.read_u16() * 15000) // 65535

    frequency = 0

    for i in range(7):

        if buttons[i].value() == 0:

            frequency = frequencies[i]

            frequency = frequency * (
                2 ** (octave - 4)
            )

            break

    if square_switch.value() == 1:
        sound = 2

    elif saw_switch.value() == 1:
        sound = 3

    else:
        sound = 1

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

            phase += (
                2
                * math.pi
                * frequency
                / sample_rate
            )

            if phase >= 2 * math.pi:
                phase -= 2 * math.pi

        else:

            value = 0

        samples += struct.pack(
            "<h",
            value
        )

    audio.write(samples)