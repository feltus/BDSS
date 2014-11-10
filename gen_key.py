import os
import yaml

app_config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'BDSS', 'config', 'app.yml')

app_config = yaml.load(open(app_config_path, 'r').read())

app_config['secret_key'] = os.urandom(24)

yaml.dump(app_config, open(app_config_path, 'w'))
