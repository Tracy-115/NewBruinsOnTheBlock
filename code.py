import board
import digitalio
import analogio
import audiobusio
import audiomixer
import synthio
import math
import time
import random
from array import array

SAMPLE_RATE = 22050

audio = audiobusio.I2SOut(
    bit_clock=board.GP1,
    word_select=board.GP2,
    data=board.GP0
)

mixer = audiomixer.Mixer(
    voice_count=1,
    sample_rate=SAMPLE_RATE,
    channel_count=1,
    bits_per_sample=16,
    samples_signed=True,
    buffer_size=2048
)

audio.play(mixer)

synth = synthio.Synthesizer(
    sample_rate=SAMPLE_RATE,
    channel_count=1
)

mixer.voice[0].play(
    synth,
    loop=True
)

volume_slider = analogio.AnalogIn(
    board.GP26
)

joystick_x = analogio.AnalogIn(
    board.GP27
)

button_pins = [
    board.GP3,
    board.GP4,
    board.GP5,
    board.GP6,
    board.GP7,
    board.GP8,
    board.GP10
]

buttons = []

for pin in button_pins:

    button = digitalio.DigitalInOut(pin)

    button.direction = (
        digitalio.Direction.INPUT
    )

    button.pull = (
        digitalio.Pull.UP
    )

    buttons.append(button)


def make_switch(pin):

    switch = digitalio.DigitalInOut(pin)

    switch.direction = (
        digitalio.Direction.INPUT
    )

    switch.pull = (
        digitalio.Pull.UP
    )

    return switch


vibrato_switch = make_switch(
    board.GP11
)

distortion_switch = make_switch(
    board.GP12
)

tremolo_switch = make_switch(
    board.GP13
)


row_pins = [
    board.GP16,
    board.GP17,
    board.GP18,
    board.GP19
]

col_pins = [
    board.GP20,
    board.GP21,
    board.GP22
]

keypad_rows = []
keypad_cols = []

for pin in row_pins:

    row = digitalio.DigitalInOut(pin)

    row.direction = (
        digitalio.Direction.OUTPUT
    )

    row.value = True

    keypad_rows.append(row)


for pin in col_pins:

    col = digitalio.DigitalInOut(pin)

    col.direction = (
        digitalio.Direction.INPUT
    )

    col.pull = (
        digitalio.Pull.UP
    )

    keypad_cols.append(col)


keys = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["*", "0", "#"]
]


frequencies = [
    261.63,
    293.66,
    329.63,
    349.23,
    392.00,
    440.00,
    493.88
]


WAVE_SIZE = 256

piano_wave = array(
    "h",
    [0] * WAVE_SIZE
)

distortion_wave = array(
    "h",
    [0] * WAVE_SIZE
)

noise_wave = array(
    "h",
    [0] * WAVE_SIZE
)


for i in range(WAVE_SIZE):

    phase = (
        2
        * math.pi
        * i
        / WAVE_SIZE
    )

    piano = (
        math.sin(phase) * 0.82
        + math.sin(phase * 2) * 0.13
        + math.sin(phase * 3) * 0.05
    )

    piano_wave[i] = int(
        piano * 28000
    )

    distortion_wave[i] = (
        32000
        if math.sin(phase) >= 0
        else -32000
    )

    noise_wave[i] = random.randint(
        -25000,
        25000
    )


piano_envelope = synthio.Envelope(
    attack_time=0.008,
    decay_time=0.8,
    release_time=0.25,
    attack_level=1.0,
    sustain_level=0.30
)

violin_envelope = synthio.Envelope(
    attack_time=0.08,
    decay_time=0.4,
    release_time=0.25,
    attack_level=0.7,
    sustain_level=0.55
)

kick_envelope = synthio.Envelope(
    attack_time=0.001,
    decay_time=0.15,
    release_time=0.05,
    attack_level=1.0,
    sustain_level=0.0
)

snare_envelope = synthio.Envelope(
    attack_time=0.001,
    decay_time=0.10,
    release_time=0.03,
    attack_level=0.7,
    sustain_level=0.0
)


piano_filter = synthio.Biquad(
    synthio.FilterMode.LOW_PASS,
    frequency=3000,
    Q=0.7
)


vibrato_lfo = synthio.LFO(
    rate=5.0,
    scale=0.012
)

tremolo_lfo = synthio.LFO(
    rate=6.0,
    scale=0.5,
    offset=0.5
)


octave = 4
joystick_moved = False

current_note_number = -1
current_note = None

last_key = None

pattern_mode = 0
pattern_step = 0
pattern_repeat = 0

step_time = 0.18
last_pattern_time = time.monotonic()

pattern_notes = []


def read_keypad():

    pressed = None

    for row in keypad_rows:
        row.value = True

    for r in range(4):

        keypad_rows[r].value = False

        for c in range(3):

            if not keypad_cols[c].value:
                pressed = keys[r][c]

        keypad_rows[r].value = True

    return pressed


def release_pattern_notes():

    global pattern_notes

    if pattern_notes:

        synth.release(
            pattern_notes
        )

        pattern_notes = []


def drum_kick():

    note = synthio.Note(
        frequency=65,
        waveform=piano_wave,
        envelope=kick_envelope,
        amplitude=0.8
    )

    synth.press(note)

    pattern_notes.append(note)


def drum_snare():

    note = synthio.Note(
        frequency=220,
        waveform=noise_wave,
        envelope=snare_envelope,
        amplitude=0.35
    )

    synth.press(note)

    pattern_notes.append(note)


def drum_hat():

    note = synthio.Note(
        frequency=1200,
        waveform=noise_wave,
        envelope=snare_envelope,
        amplitude=0.15
    )

    synth.press(note)

    pattern_notes.append(note)


def violin(freq):

    note = synthio.Note(
        frequency=freq,
        waveform=piano_wave,
        envelope=violin_envelope,
        amplitude=0.25,
        filter=piano_filter
    )

    synth.press(note)

    pattern_notes.append(note)


def trigger_step():

    global pattern_step
    global pattern_repeat
    global pattern_mode

    release_pattern_notes()

    if pattern_mode == 1:

        if pattern_step in [0, 4]:
            drum_kick()

        if pattern_step in [2, 6]:
            drum_snare()

        if pattern_step % 2 == 0:
            drum_hat()

    elif pattern_mode == 2:

        if pattern_step in [
            0,
            2,
            4,
            6
        ]:
            drum_kick()

        if pattern_step in [
            3,
            7
        ]:
            drum_snare()

    elif pattern_mode == 3:

        if pattern_step in [
            0,
            3,
            4
        ]:
            drum_kick()

        if pattern_step in [
            2,
            6
        ]:
            drum_snare()

        drum_hat()

    elif pattern_mode == 4:

        if pattern_step in [0, 4]:
            drum_kick()

        if pattern_step in [2, 6]:
            drum_snare()

        violin(196)

    elif pattern_mode == 5:

        if pattern_step in [0, 4]:
            drum_kick()

        if pattern_step in [2, 6]:
            drum_snare()

        violin(247)

    elif pattern_mode == 7:

        if pattern_step in [0, 4]:
            drum_kick()

        if pattern_step in [2, 6]:
            drum_snare()

        violin(330)

    elif pattern_mode == 8:

        violin_notes = [
            196,
            220,
            247,
            262,
            247,
            220,
            196,
            165
        ]

        if pattern_step in [0, 4]:
            drum_kick()

        if pattern_step in [2, 6]:
            drum_snare()

        violin(
            violin_notes[
                pattern_step
            ]
        )

    pattern_step += 1

    if pattern_step >= 8:

        pattern_step = 0
        pattern_repeat += 1

        if pattern_repeat >= 3:

            pattern_mode = 0

            release_pattern_notes()


def start_piano_note(
    frequency
):

    global current_note

    vibrato_on = (
        vibrato_switch.value
    )

    distortion_on = (
        distortion_switch.value
    )

    tremolo_on = (
        tremolo_switch.value
    )

    waveform = piano_wave

    bend = 0.0
    amplitude = 0.85

    if distortion_on:
        waveform = distortion_wave
        amplitude = 1.0

    if vibrato_on:
        bend = vibrato_lfo

    if tremolo_on:
        amplitude = tremolo_lfo

    current_note = synthio.Note(
        frequency=frequency,
        waveform=waveform,
        envelope=piano_envelope,
        amplitude=amplitude,
        bend=bend,
        filter=piano_filter
    )

    synth.press(
        current_note
    )


def stop_piano_note():

    global current_note

    if current_note is not None:

        synth.release(
            current_note
        )

        current_note = None


print(
    "CircuitPython instrument ready"
)

print(
    "Octave:",
    octave
)


while True:

    volume = (
        volume_slider.value
        / 65535
    )

    mixer.voice[0].level = volume


    joystick_value = (
        joystick_x.value
    )

    if not joystick_moved:

        if joystick_value > 50000:

            octave -= 1

            if octave < 1:
                octave = 1

            joystick_moved = True

            print(
                "Octave:",
                octave
            )

        elif joystick_value < 15000:

            octave += 1

            if octave > 8:
                octave = 8

            joystick_moved = True

            print(
                "Octave:",
                octave
            )

    if (
        25000
        < joystick_value
        < 40000
    ):
        joystick_moved = False


    note_number = -1

    for i in range(7):

        if not buttons[i].value:

            note_number = i
            break


    if (
        note_number != -1
        and note_number
        != current_note_number
    ):

        stop_piano_note()

        frequency = (
            frequencies[note_number]
            * (
                2
                ** (
                    octave - 4
                )
            )
        )

        start_piano_note(
            frequency
        )

        print(
            ["C", "D", "E", "F", "G", "A", "B"][note_number]
        )

        current_note_number = (
            note_number
        )


    elif note_number == -1:

        if (
            current_note_number
            != -1
        ):

            stop_piano_note()

        current_note_number = -1


    key = read_keypad()

    if (
        key is not None
        and key != last_key
    ):

        print(
            "Keypad:",
            key
        )

        if key == "1":
            pattern_mode = 1

        elif key == "2":
            pattern_mode = 2

        elif key == "3":
            pattern_mode = 3

        elif key == "4":
            pattern_mode = 4

        elif key == "5":
            pattern_mode = 5

        elif key == "7":
            pattern_mode = 7

        elif key == "8":
            pattern_mode = 8

        elif key == "0":

            pattern_mode = 0

            release_pattern_notes()

        if key in [
            "1",
            "2",
            "3",
            "4",
            "5",
            "7",
            "8"
        ]:

            pattern_step = 0
            pattern_repeat = 0

            trigger_step()

            last_pattern_time = (
                time.monotonic()
            )

        last_key = key


    if key is None:
        last_key = None


    if pattern_mode != 0:

        if (
            time.monotonic()
            - last_pattern_time
            >= step_time
        ):

            last_pattern_time = (
                time.monotonic()
            )

            trigger_step()


    time.sleep(0.002)