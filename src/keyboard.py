import peripherals
import midi_player
import common

CHANNEL = 1
MIDI_BASS_DRUM = 36
MIDI_ACCOUSTIC_SNARE = 38
MIDI_HIGH_TOM = 50
MIDI_LOW_TOM = 45
MIDI_CRASH_CYMBAL = 49
MIDI_RIDE_CYMBAL = 51

HIGH_VELOCITY = 100
LOW_VELOCITY = 64


def on_button_change(index, state):
    midi_index = 0
    velocity = 0
    if index == 0:
        midi_index = MIDI_LOW_TOM
        velocity = HIGH_VELOCITY
    elif index == 1:
        midi_index = MIDI_HIGH_TOM
        velocity = HIGH_VELOCITY
    elif index == 2:
        midi_index = MIDI_ACCOUSTIC_SNARE
        velocity = HIGH_VELOCITY
    elif index == 3:
        midi_index = MIDI_BASS_DRUM
        velocity = HIGH_VELOCITY

    elif index == 4:
        midi_index = MIDI_LOW_TOM
        velocity = LOW_VELOCITY
    elif index == 5:
        midi_index = MIDI_HIGH_TOM
        velocity = LOW_VELOCITY
    elif index == 6:
        midi_index = MIDI_ACCOUSTIC_SNARE
        velocity = LOW_VELOCITY
    elif index == 7:
        midi_index = MIDI_BASS_DRUM
        velocity = LOW_VELOCITY

    elif index == 8:
        midi_index = MIDI_RIDE_CYMBAL
        velocity = HIGH_VELOCITY
    elif index == 9:
        midi_index = MIDI_CRASH_CYMBAL
        velocity = HIGH_VELOCITY
    if state:
        midi_player.note_on(CHANNEL, midi_index, velocity)
    else:
        midi_player.note_off(CHANNEL, midi_index)


def init():
    peripherals.register_on_button_change_cb(on_button_change)


def loop():
    pass
