import json


def extract_key_value(key):
    """Extracts a specific key-value pair from a JSON data"""
    try:
        with open("config.json") as conf_file:
            data = json.loads(conf_file.read())
            value = data.get(key)
            return value
    except:
        pass


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
                for k, v in json.loads(conf_file.read()).items():
                    setattr(self, k, v)
        except Exception as e:
            print(f"Error was detected while reading {config_file_name}: {str(e)}. Hard coded values will be applied")

    def save_config_file(self, config_file_name: str = "config.json"):
        try:
            conf_items = {k: v for k, v in vars(self).items() if isinstance(v, (int, float, str, list, dict))}
            with open(config_file_name, "w") as conf_file:
                json.dump(conf_items, conf_file, sort_keys=False, indent=2)
        except Exception as e:
            print(f"Error was detected while saving {config_file_name}: {str(e)}")
