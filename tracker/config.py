from configparser import ConfigParser
from os import path
from pathlib import Path


_DEFAULT = "DEFAULT"

_LOG_FILE = "LOG_FILE"
_DB_FILE = "DB_FILE"
_IMGS_FOLDER = "IMGS_FOLDER"
_TELEGRAM_TOKEN = "TELEGRAM_TOKEN"
_TELEGRAM_CHATID = "TELEGRAM_CHATID"

# ---------------------------------------------------------


class EnvConfig:
    def __init__(self):
        self.current_conf = ConfigParser()

        dir_path = path.dirname(path.abspath(__file__))
        config_file = Path(dir_path, "..", "config.ini")
        if not config_file.exists():
            raise RuntimeError(f"config file '{config_file}' not found")

        self.setup(config_file)

    def setup(self, config_path: Path):
        self.current_conf.read(config_path)

    def get_log_file(self) -> str:
        return self.current_conf[_DEFAULT][_LOG_FILE]

    def get_db_file(self) -> str:
        return self.current_conf[_DEFAULT][_DB_FILE]

    def get_imgs_folder(self) -> str:
        return self.current_conf[_DEFAULT][_IMGS_FOLDER]

    def get_telegram_token(self) -> str:
        return self.current_conf[_DEFAULT][_TELEGRAM_TOKEN]

    def get_telegram_chat_id(self) -> str:
        return self.current_conf[_DEFAULT][_TELEGRAM_CHATID]


class CurrentConf:
    """
    Singleton class for the current configuration
    """

    __current_conf = None

    @staticmethod
    def get() -> EnvConfig:
        if not CurrentConf.__current_conf:
            CurrentConf.__current_conf = EnvConfig()
        return CurrentConf.__current_conf

    def __init__(self):
        raise RuntimeError("__init__ method not enabled")
