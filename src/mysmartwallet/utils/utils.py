import os
import sys


def get_base_path():
    """Get base path of the project

    Returns
    -------
    str
        Base path of the projet
    """
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(__file__)
    return base_path

def get_config_path():
    """Get config file path

    Returns
    -------
    str
        Path of the config file
    """
    base_path = get_base_path()
    if getattr(sys, 'frozen', False):
        config_path = os.path.join(base_path, "config.ini")
    else:
        config_path = os.path.join(base_path, '..', '..', '..', 'config', 'config.ini')
    return config_path

if __name__ == "__main__":
    config_dir = os.path.dirname(get_config_path())
    print(config_dir, os.listdir(config_dir))