import json

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfigHandler:
    def __init__(self, filename="config.json"):
        self.filename = filename

        with open('config.json') as config_file:
            self.config = json.load(config_file)

    def get_value(self, section, key):
        try:
            value = self.config[section][key]
        except KeyError:
            logger.warning(f"KeyError when trying to access config->{section}->{key}.")
            value = None

        return value

    def set_value(self, section, key, value):
        self.config[section][key] = value

        # Save to file
        with open(self.filename, 'w') as outfile:
            json.dump(self.config, outfile, indent=4, sort_keys=True)
