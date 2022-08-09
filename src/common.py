import digitalio
import analogio
from board import *
import time
import usb_midi

# import busio

LED_PIN = GP25
BUTTONS = [GP6, GP7, GP8, GP9, GP2, GP3, GP4, GP5, GP0, GP1]
OUTPUT = GP12


# uart = busio.UART(GP0, GP1, baudrate=31250)


def get_millis():
    return int(time.monotonic_ns() / 1000 / 1000)


def millis_passed(timestamp):
    return get_millis() - timestamp


def create_output(pin):
    gpio_out = digitalio.DigitalInOut(pin)
    gpio_out.direction = digitalio.Direction.OUTPUT
    return gpio_out


def create_input(pin):
    gpio_in = digitalio.DigitalInOut(pin)
    gpio_in.direction = digitalio.Direction.INPUT
    gpio_in.pull = digitalio.Pull.DOWN
    return gpio_in


def create_analog_input(pin):
    analog_in = analogio.AnalogIn(pin)
    return analog_in


def remap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def remap_pot(x):
    return remap(x, 0, 65535, 0, 127)


def get_pot_mean(pot, counts):
    measures = [remap_pot(pot.value) for i in range(counts)]
    measures.sort()
    for i in range(counts / 4):
        measures.pop(0)
        measures.pop(-1)
    return int(sum(measures) / len(measures))


def test_peripherals():
    buttons_select = []
    buttons_data = []
    buttons_state = {}
    for pin in BUTTON_SELECT:
        buttons_select.append(create_output(pin))
        buttons_select[-1].value = False
    for pin in BUTTON_DATA:
        buttons_data.append(create_input(pin))
    for select_index, select in enumerate(buttons_select):
        for data_index, data in enumerate(buttons_data):
            buttons_state[(select_index, data_index)] = -1

    pots = []
    pots_state = {}
    for pin in POTS:
        pots.append(create_analog_input(pin))
    for pot_index, pot in enumerate(pots):
        pots_state[pot_index] = -1

    while True:
        for select_index, select in enumerate(buttons_select):
            select.value = True
            for data_index, data in enumerate(buttons_data):
                state = data.value
                if state != buttons_state[(select_index, data_index)]:
                    print("button changed[%d:%d] = %d" %
                          (select_index, data_index, state))
                    buttons_state[(select_index, data_index)] = state
            select.value = False

        for pot_index, pot in enumerate(pots):
            state = get_pot_mean(pot, POT_MEASURE_COUNTS)
            if abs(state - pots_state[pot_index]) >= 1:
                pots_state[pot_index] = state
                print("pot changed[%d] = %d" %
                      (pot_index, pots_state[pot_index]))


def send_usb_midi_message(data):
    usb_midi.ports[1].write(bytearray(data))

# def send_raw_midi_message(data):
#    uart.write(bytearray(data))
