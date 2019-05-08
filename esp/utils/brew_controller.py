from utils.pins import RELAY
from utils.user_config import UserConfig


class BrewController:
    def __init__(self):
        self.user_conf = UserConfig()

        self.is_brewing = False

    @property
    def brew_time(self):
        self.user_conf.reload()
        return self.user_conf.get()['brew_time']

    def start_brewing(self):
        if self.is_brewing:
            return False

        RELAY.open_for_duration(self.brew_time)
        self.is_brewing = True

        return True

    def stop_brewing(self):
        RELAY.close()
        self.is_brewing = False


BREW_CONTROLLER = BrewController()
