__name__ = "MySmartWallet"
__author__ = "Clément Peillon"
__license__ = "MIT"

version_dict = {
    "major": 0,
    "minor": 1,
    "patch": 0,
}

__version__ = "{major}.{minor}.{patch}".format(**version_dict)


def getVersion():
    return __version__


def getApplicationName():
    return __name__


def getAuthor():
    return __author__


def getLicense():
    return __license__
