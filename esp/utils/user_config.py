import copy
import json
from uerrno import ENOENT


class UserConfig:
    def __init__(self, filename='userconf.json'):
        self.filename = filename

        self.__conf = {}
        self._load()

    def _load(self):
        try:
            with open(self.filename) as conf_file:
                self.__conf = json.loads(conf_file.read())
        except OSError as exc:
            if exc.args[0] != ENOENT:
                raise exc

    def _save(self):
        with open(self.filename, 'w') as conf_file:
            conf_file.write(json.dumps(self.__conf))

    def get(self):
        return copy.copy(self.__conf)

    def update(self, values):
        self.__conf.update(values)
        self._save()

        if 'ssid' in values or 'password' in values:
            from utils import wifi
            wifi.connect()

    def reload(self):
        self._load()
