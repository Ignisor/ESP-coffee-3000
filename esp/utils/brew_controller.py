import machine
import time

from utils.pins import RELAY
from utils.user_config import UserConfig


class BrewController:
    def __init__(self):
        self.user_conf = UserConfig()

        self.is_brewing = False
        self.brew_start = None

    @property
    def brew_time(self):
        self.user_conf.reload()
        return self.user_conf.get()['brew_time']

    def start_brewing(self):
        if self.is_brewing:
            return False

        RELAY.open()
        RELAY.timer.init(
            period=self.brew_time * 1000,
            mode=machine.Timer.ONE_SHOT,
            callback=lambda t: self.stop_brewing()
        )

        self.is_brewing = True
        self.brew_start = time.localtime()

        return True

    def stop_brewing(self):
        RELAY.close()
        self.is_brewing = False

    @property
    def status_info(self):
        status = {
            'is_brewing': self.is_brewing,
        }

        if self.is_brewing:
            status.update({
                'brew_start': self.brew_start,
                'brew_duration': self.brew_time,
            })

        return status


BREW_CONTROLLER = BrewController()
