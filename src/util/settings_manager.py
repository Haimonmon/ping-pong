import os
import json


class SettingsManager:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        settings_dir = os.path.join(current_dir, "../data/settings")
        self.settings_dir = os.path.abspath(settings_dir)


    def load_settings(self, filename):
        """
        Load settings from a JSON file.
        """
        file_path = os.path.join(self.settings_dir, filename)
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from file '{filename}'.")
        return None


    def save_settings(self, filename, data):
        """
        Save settings to a JSON file.
        """
        file_path = os.path.join(self.settings_dir, filename)
        try:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error: Failed to save settings to '{filename}': {e}")


if __name__ == "__main__":
    manager = SettingsManager()
    appearance_settings = manager.load_settings("appearance.json")
    print("Appearance Settings:", appearance_settings['user_interface']['themes'])

