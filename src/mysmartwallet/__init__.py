__name__ = "MySmartWallet"
__author__ = "Clément Peillon"
__license__ = "MIT"

version_dict = {
    "major": 0,
    "minor": 1,
    "patch": 0,
}

__version__ = "{major}.{minor}.{patch}".format(**version_dict)

def get_version():
    return __version__

def get_application_name():
    return __name__

def get_author():
    return __author__

def get_license():
    return __license__