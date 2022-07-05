import configparser
import os

def get(section, name):
    value = None

    config = configparser.ConfigParser(allow_no_value=True)
    config.read(f'{os.getcwd()}/config/prod.config')

    value = config.get(section, name)

    return value