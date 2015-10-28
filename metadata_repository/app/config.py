import os

import yaml

app_config = {}
config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "app_config.yml")
app_config = yaml.load(open(config_path, "r").read())
