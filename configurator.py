import json

class Configurator:
    def __init__(self):
        # Hard coded values if config file doesn't exist
        self.days: int = 0
        self.hours: int = 0
        self.minutes: int = 0
        self.on_boot: bool = False
        self.latest_time: str = ''

    def read_config_file(self, config_file_name: str = "config.json"):
        try:
            with open(config_file_name) as conf_file:
                data = json.load(conf_file)
                for key, value in data.items():
                    setattr(self, key, value)
        except Exception as e:
            print(f"Error occurred while reading {config_file_name}: {str(e)}. Hard coded values will be applied.")

    def save_config_file(self, config_file_name: str = "config.json"):
        try:
            conf_items = {k: v for k, v in vars(self).items() if isinstance(v, (int, float, str, bool, list, dict))}
            with open(config_file_name, "w") as conf_file:
                json.dump(conf_items, conf_file, sort_keys=False, indent=2)
        except Exception as e:
            print(f"Error occurred while saving {config_file_name}: {str(e)}")

    def get_value(self, key):
        """Extracts a specific key-value pair from the class attributes"""
        return getattr(self, key, None)
