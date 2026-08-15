from configparser import ConfigParser

from mysmartwallet.utils.utils import get_config_path


class AppConfig:
    """Class to read the config file

    Returns
    -------
    AppConfig
    """
    _instance = None

    def __new__(cls):
        """Create a unique AppConfig instance

        Returns
        -------
        AppConfig
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = ConfigParser()
            config_file_path = get_config_path()

            cls._instance.config.read(config_file_path)
            cls._instance.ROOT_DIR = cls._instance.config.get('PATH','ROOT_DIR')
            cls._instance.DATA_DIR = cls._instance.config.get('PATH','DATA_DIR')
            cls._instance.DB_PATH = cls._instance.config.get('PATH','DB_PATH')

        return cls._instance


CONFIG = AppConfig()
            

            