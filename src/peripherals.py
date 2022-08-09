import common

buttons = []
on_button_change_cb = None
output = None


class Button:
    def __init__(self, pin, index):
        self.pin = common.create_input(pin)
        self.state = -1
        self.index = index

    def read(self):
        return self.pin.value

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_index(self):
        return self.index


def init():
    global buttons_state, output
    output = common.create_output(common.OUTPUT)
    output.value = True
    for index, pin in enumerate(common.BUTTONS):
        buttons.append(Button(pin, index))


def loop():
    global buttons
    global on_button_change_cb, on_pot_change_cb
    for button in buttons:
        state = button.read()
        if state != button.get_state():
            button.set_state(state)
            print("button changed[%d] = %d" % (button.get_index(), button.get_state()))
            if on_button_change_cb:
                on_button_change_cb(button.get_index(), button.get_state())


def register_on_button_change_cb(cb):
    global on_button_change_cb
    on_button_change_cb = cb


def test_loop():
    init()
    while True:
        loop()
