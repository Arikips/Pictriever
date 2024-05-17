import json
import os

class Settings:
    def __init__(self, config_file='settings.json'):
        self.config_file = config_file
        self.load_settings()

    def load_settings(self):
        if not os.path.exists(self.config_file):
            self.hotkeys = {
                'select_area': 'ctrl+alt+s',
                'scan_area': 'ctrl+alt+x',
                'terminate_app': 'ctrl+alt+q'
            }
            self.save_settings()
        else:
            with open(self.config_file, 'r') as f:
                self.hotkeys = json.load(f)

    def save_settings(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.hotkeys, f, indent=4)
