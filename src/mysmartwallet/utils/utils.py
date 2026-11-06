import sys
from pathlib import Path


def getBasePath():
    """Get base path of the project

    Returns
    -------
    str
        Base path of the projet
    """

    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent

    return Path(__file__).resolve().parents[3]


def getConfigPath():
    """Get config file path

    Returns
    -------
    str
        Path of the config file
    """
    basePath = getBasePath()
    if getattr(sys, "frozen", False):
        return basePath / "config.ini"
    return basePath / "config/config.ini"


if __name__ == "__main__":
    print(getBasePath())
    print(getConfigPath())
