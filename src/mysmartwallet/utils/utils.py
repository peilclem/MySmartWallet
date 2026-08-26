from pathlib import Path
import sys


def get_base_path():
    """Get base path of the project

    Returns
    -------
    str
        Base path of the projet
    """
    
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent

    return Path(__file__).resolve().parents[3]

def get_config_path():
    """Get config file path

    Returns
    -------
    str
        Path of the config file
    """
    base_path = get_base_path()
    if getattr(sys, 'frozen', False):
        return base_path / "config.ini"
    return base_path / "config/config.ini"

if __name__ == "__main__":
    print(get_base_path())
    print(get_config_path())