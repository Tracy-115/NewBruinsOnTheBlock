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
joystick_x = ADC(27)

buttons = [
    Pin(3, Pin.IN, Pin.PULL_UP),
    Pin(4, Pin.IN, Pin.PULL_UP),
    Pin(5, Pin.IN, Pin.PULL_UP),
    Pin(6, Pin.IN, Pin.PULL_UP),
    Pin(7, Pin.IN, Pin.PULL_UP),
    Pin(8, Pin.IN, Pin.PULL_UP),
    Pin(10, Pin.IN, Pin.PULL_UP)
]

vibrato_switch = Pin(11, Pin.IN, Pin.PULL_UP)
distortion_switch = Pin(12, Pin.IN, Pin.PULL_UP)
tremolo_switch = Pin(13, Pin.IN, Pin.PULL_UP)

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
tremolo_phase = 0

octave = 1
joystick_moved = False

print("Synthesizer Ready")
print("Octave:", octave)

while True:

    joystick_value = joystick_x.read_u16()

    if not joystick_moved:

        if joystick_value > 50000:

            octave += 1

            if octave > 8:
                octave = 8

            joystick_moved = True
            print("Octave:", octave)

        elif joystick_value < 15000:

            octave -= 1

            if octave < 1:
                octave = 1

            joystick_moved = True
            print("Octave:", octave)

    if 25000 < joystick_value < 40000:
        joystick_moved = False

    volume = (
        potent.read_u16()
        * 15000
    ) // 65535

    frequency = 0

    for i in range(7):

        if buttons[i].value() == 0:

            frequency = frequencies[i]

            frequency = frequency * (
                2 ** (octave - 4)
            )

            break

    vibrato_on = vibrato_switch.value() == 0
    distortion_on = distortion_switch.value() == 0
    tremolo_on = tremolo_switch.value() == 0

    samples = bytearray()

    for i in range(chunk_size):

        if frequency > 0:

            current_frequency = frequency

            if vibrato_on:

                vibrato = (
                    math.sin(vibrato_phase)
                    * frequency
                    * 0.04
                )

                current_frequency += vibrato

                vibrato_phase += (
                    2
                    * math.pi
                    * 5
                    / sample_rate
                )

                if vibrato_phase >= 2 * math.pi:
                    vibrato_phase -= 2 * math.pi

            wave = math.sin(phase)

            if distortion_on:

                wave = wave * 3

                wave = wave / (
                    1 + abs(wave)
                )

            if tremolo_on:

                tremolo = (
                    0.65
                    + 0.35
                    * math.sin(tremolo_phase)
                )

                wave = wave * tremolo

                tremolo_phase += (
                    2
                    * math.pi
                    * 4
                    / sample_rate
                )

                if tremolo_phase >= 2 * math.pi:
                    tremolo_phase -= 2 * math.pi

            value = int(
                volume * wave
            )

            phase += (
                2
                * math.pi
                * current_frequency
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