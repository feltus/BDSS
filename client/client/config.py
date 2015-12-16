import configparser
import os
from pkg_resources import resource_string

config = configparser.ConfigParser()
config.read_string(resource_string(__name__, "defaults.cfg").decode("utf-8"))
config.read([os.path.expanduser("~/.bdss.cfg"), "bdss.cfg"])

metadata_repository_url = config.get("metadata_repository", "url").rstrip("/")
