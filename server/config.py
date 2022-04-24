import yaml


def read_config():
    with open('config.yaml') as stream:
        return yaml.safe_load(stream)
