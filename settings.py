import copy
import json
import os
from pathlib import Path


def _load():
    p = os.path.join(Path(__file__).parent.absolute(), 'conf', 'settings.json')
    with open(p, 'r+') as f:
        loaded = json.load(f)
    return loaded


def get(setting_name, default=None, required=True):
    result = _settings.get(setting_name)
    result = copy.copy(result) if result is not None else default

    if required and result is None:
        raise SettingNotSetException(f'Unable to read the required setting by name={setting_name}')

    return result


class SettingNotSetException(Exception):
    pass


_settings = _load()
