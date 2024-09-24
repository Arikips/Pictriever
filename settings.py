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
                'terminate_app': 'ctrl+alt+q',
                'toggle_auto_scan': 'ctrl+alt+a'
            }
            self.auto_scan_interval = 2
            self.save_settings()
        else:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                self.hotkeys = {
                    'select_area': data.get('select_area', 'ctrl+alt+s'),
                    'scan_area': data.get('scan_area', 'ctrl+alt+x'),
                    'terminate_app': data.get('terminate_app', 'ctrl+alt+q'),
                    'toggle_auto_scan': data.get('toggle_auto_scan', 'ctrl+alt+a')
                }
                self.auto_scan_interval = data.get('auto_scan_interval', 10)

    def save_settings(self):
        data = {
            'select_area': self.hotkeys['select_area'],
            'scan_area': self.hotkeys['scan_area'],
            'terminate_app': self.hotkeys['terminate_app'],
            'toggle_auto_scan': self.hotkeys['toggle_auto_scan'],
            'auto_scan_interval': self.auto_scan_interval
        }
        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=4)
