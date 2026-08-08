from machine import I2S, Pin, ADC
import math
import struct
import random
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

keypad_rows = [
    Pin(16, Pin.OUT),
    Pin(17, Pin.OUT),
    Pin(18, Pin.OUT),
    Pin(19, Pin.OUT)
]

keypad_cols = [
    Pin(20, Pin.IN, Pin.PULL_UP),
    Pin(21, Pin.IN, Pin.PULL_UP),
    Pin(22, Pin.IN, Pin.PULL_UP)
]

keys = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["*", "0", "#"]
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

bass_notes = [
    82,
    98,
    110,
    123,
    110,
    98,
    82,
    98
]

phase = 0
bass_phase = 0
vibrato_phase = 0
tremolo_phase = 0
kick_phase = 0

octave = 1
joystick_moved = False

last_note = -1
envelope = 0

last_key = None

pattern_mode = 0
pattern_step = 0
pattern_repeat = 0
last_pattern_step = time.ticks_ms()

bass_frequency = 0

kick_level = 0
snare_level = 0
hat_level = 0

step_time = 180

print("Octave:", octave)


def read_keypad():

    pressed = None

    for row in keypad_rows:
        row.value(1)

    for r in range(4):

        keypad_rows[r].value(0)

        for c in range(3):

            if keypad_cols[c].value() == 0:
                pressed = keys[r][c]

        keypad_rows[r].value(1)

    return pressed


def trigger_step():

    global pattern_step
    global pattern_repeat
    global pattern_mode
    global bass_frequency
    global kick_level
    global snare_level
    global hat_level

    bass_frequency = 0

    if pattern_mode == 1 or pattern_mode == 3:

        if pattern_step == 0 or pattern_step == 4:
            kick_level = 1.0

        if pattern_step == 2 or pattern_step == 6:
            snare_level = 1.0

        hat_level = 1.0

    if pattern_mode == 2 or pattern_mode == 3:
        bass_frequency = bass_notes[pattern_step]

    pattern_step += 1

    if pattern_step >= 8:

        pattern_step = 0
        pattern_repeat += 1

        if pattern_repeat >= 3:
            pattern_mode = 0
            bass_frequency = 0


while True:

    key = read_keypad()

    if key is not None and key != last_key:

        print("Keypad:", key)

        if key == "1":

            pattern_mode = 1
            pattern_step = 0
            pattern_repeat = 0

            trigger_step()

            last_pattern_step = time.ticks_ms()

        elif key == "2":

            pattern_mode = 2
            pattern_step = 0
            pattern_repeat = 0

            trigger_step()

            last_pattern_step = time.ticks_ms()

        elif key == "3":

            pattern_mode = 3
            pattern_step = 0
            pattern_repeat = 0

            trigger_step()

            last_pattern_step = time.ticks_ms()

        elif key == "0":

            pattern_mode = 0
            bass_frequency = 0
            kick_level = 0
            snare_level = 0
            hat_level = 0

        last_key = key

    if key is None:
        last_key = None

    if pattern_mode != 0:

        if time.ticks_diff(
            time.ticks_ms(),
            last_pattern_step
        ) >= step_time:

            last_pattern_step = time.ticks_ms()

            trigger_step()

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
    note_number = -1

    for i in range(7):

        if buttons[i].value() == 0:

            note_number = i

            frequency = frequencies[i] * (
                2 ** (octave - 4)
            )

            break

    if note_number != -1 and note_number != last_note:
        envelope = 1.0
        phase = 0

    if note_number == -1:
        envelope = 0

    last_note = note_number

    vibrato_on = vibrato_switch.value() == 1
    distortion_on = distortion_switch.value() == 1
    tremolo_on = tremolo_switch.value() == 1

    samples = bytearray()

    for i in range(chunk_size):

        synth_wave = 0
        bass_wave = 0
        drum_wave = 0

        if frequency > 0:

            current_frequency = frequency

            if vibrato_on:

                current_frequency = (
                    frequency
                    + math.sin(vibrato_phase)
                    * frequency
                    * 0.06
                )

                vibrato_phase += (
                    2
                    * math.pi
                    * 5
                    / sample_rate
                )

                if vibrato_phase >= 2 * math.pi:
                    vibrato_phase -= 2 * math.pi

            synth_wave = (
                math.sin(phase) * 0.65
                + math.sin(phase * 2) * 0.22
                + math.sin(phase * 3) * 0.10
                + math.sin(phase * 4) * 0.03
            )

            if envelope > 0.25:
                envelope *= 0.9997

            synth_wave *= envelope

            if distortion_on:

                synth_wave *= 5

                if synth_wave > 0.65:
                    synth_wave = 0.65

                elif synth_wave < -0.65:
                    synth_wave = -0.65

                synth_wave /= 0.65

            if tremolo_on:

                tremolo = (
                    0.525
                    + 0.475
                    * math.sin(tremolo_phase)
                )

                synth_wave *= tremolo

                tremolo_phase += (
                    2
                    * math.pi
                    * 6
                    / sample_rate
                )

                if tremolo_phase >= 2 * math.pi:
                    tremolo_phase -= 2 * math.pi

            phase += (
                2
                * math.pi
                * current_frequency
                / sample_rate
            )

            if phase >= 2 * math.pi:
                phase -= 2 * math.pi

        if bass_frequency > 0:

            bass_wave = (
                math.sin(bass_phase) * 0.7
                + math.sin(bass_phase * 2) * 0.3
            )

            bass_phase += (
                2
                * math.pi
                * bass_frequency
                / sample_rate
            )

            if bass_phase >= 2 * math.pi:
                bass_phase -= 2 * math.pi

        if kick_level > 0.01:

            drum_wave += (
                math.sin(kick_phase)
                * kick_level
                * 1.3
            )

            kick_frequency = (
                55
                + 90 * kick_level
            )

            kick_phase += (
                2
                * math.pi
                * kick_frequency
                / sample_rate
            )

            if kick_phase >= 2 * math.pi:
                kick_phase -= 2 * math.pi

            kick_level *= 0.988

        if snare_level > 0.01:

            drum_wave += (
                random.randint(-1000, 1000)
                / 1000
                * snare_level
                * 1.1
            )

            snare_level *= 0.975

        if hat_level > 0.01:

            drum_wave += (
                random.randint(-1000, 1000)
                / 1000
                * hat_level
                * 0.35
            )

            hat_level *= 0.90

        mixed = (
            synth_wave * 0.50
            + bass_wave * 0.70
            + drum_wave * 0.65
        )

        value = int(
            volume * mixed
        )

        if value > 32767:
            value = 32767

        elif value < -32768:
            value = -32768

        samples += struct.pack(
            "<h",
            value
        )

    audio.write(samples)