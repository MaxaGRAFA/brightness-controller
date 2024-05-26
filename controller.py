import screen_brightness_control as sbc

from typing import Tuple, List

import json

class BrightnessController():
    def __init__(self) -> None:
        self.ModeManager = ModeManager() 

    def set_mode(self, mode_index: int) -> None:
        """Sets brightness according to mode"""
        mode = self.ModeManager.get_mode(mode_index)

        if len(mode[1]) != len(self.get_monitors()):
            raise Exception('Incompatible number of monitors')

        for i, perc in enumerate(mode[1]):
            self.set_brightness(perc, i)
        

    def set_brightness(self, percentage: int, display: int) -> None:
        sbc.set_brightness(percentage, display)

    def create_new_mode(self, name: str, brightness: list) -> None:
        self.ModeManager.save_new_mode(name, brightness)

    def get_monitors(self) -> list:
        return sbc.list_monitors()
    
    def get_brightness(self, monitor: int) -> int:
        return sbc.get_brightness()[int(monitor)]
    
class ModeManager():
    def __init__(self) -> None:
        self.jsonfile = 'modes_storage.json'
    
    def save_new_mode(self, name: str, brightness: list) -> None:
        """Saves the mode to a json file"""
        data = self._load_json()
        data[name] = brightness

        self._save_data_(data)

    def get_mode(self, index: int) -> Tuple[str, List[int]]:
        """Returns brightness and mode name by index"""
        data = self._load_json()
        mode_name = list(data)[index]
        brightness = data[mode_name]

        return mode_name, brightness
    
    def get_all_modes(self) -> dict:
        data = self._load_json()
        return data

    def delete_mode(self, name: str) -> None:
        data = self._load_json()
        del data[name]

        self._save_data_(data)

    def _repair_empty_file(self) -> None:
        data = {'Evening': [20, 20], 'Morning': [50, 50]}

        self._save_data_(data)

    def _load_json(self) -> dict:
        try:
            with open(self.jsonfile, 'r') as jsonFile:
                data = json.load(jsonFile)
        except json.decoder.JSONDecodeError: 
            self._repair_empty_file()
            data = self._load_json()

        return data
    
    def _save_data_(self, data: dict) -> None:
        with open(self.jsonfile, 'w') as jsonFile:
            json.dump(data, jsonFile)