import machine


ON = 1
OFF = 0

LED = machine.Pin(1, machine.Pin.OUT)


class RelayController:
    OPEN = b'\xA0\x01\x00\xA1'
    CLOSE = b'\xA0\x01\x01\xA2'

    def __init__(self):
        self.timer = machine.Timer(-1)
        self.opened = False
        self._relay = None

    def __lazy_init_uart(self):
        self._relay = machine.UART(0, 9600)
        self._relay.init(9600, bits=8, parity=None, stop=1, timeout=10)
        self._relay.write(self.OPEN)

    @property
    def relay(self):
        if self._relay is None:
            self.__lazy_init_uart()

        return self._relay

    def open(self):
        self.relay.write(self.OPEN)
        self.opened = True

    def close(self):
        self.relay.write(self.CLOSE)
        self.opened = False

        self.timer.deinit()  # interrupt time in case open_for_duration is going on

    def open_for_duration(self, duration):
        """
        Opens relay for some duration. Will not open if already opened.
        :param duration: time in seconds
        :return: boolean, True if opened, False if not
        """
        if self.opened:
            return False  # don't open if already opened

        self.open()
        self.timer.init(period=duration * 1000, mode=machine.Timer.ONE_SHOT, callback=lambda t: self.close())

        return True


RELAY = RelayController()
