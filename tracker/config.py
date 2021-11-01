from configparser import ConfigParser
from os import path
from pathlib import Path


_DEFAULT = "DEFAULT"

_LOG_FILE = "LOG_FILE"
_DB_FILE = "DB_FILE"
_TELEGRAM_TOKEN = "TELEGRAM_TOKEN"
_TELEGRAM_CHATID = "TELEGRAM_CHATID"

# ---------------------------------------------------------

class EnvConfig:
    def __init__(self):
        self.current_conf = ConfigParser()

        current_path = path.abspath(__file__)
        dir_path = path.dirname(current_path)

        # Check the absolute file into the package
        config_file = Path(dir_path, "..", "config.ini")
        if not config_file.exists():
            raise RuntimeError(f"config file '{config_file}' not found")

        # setup with config file
        self.setup(config_file)

    def setup(self, config_path: Path):
        self.current_conf.read(config_path)

    def get_log_file(self) -> str:
        return self.current_conf[_DEFAULT][_LOG_FILE]

    def get_db_file(self) -> str:
        return self.current_conf[_DEFAULT][_DB_FILE]
    
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
        if CurrentConf.__current_conf is None:
            CurrentConf.__current_conf = EnvConfig()

        return CurrentConf.__current_conf

    def __init__(self):
        raise RuntimeError("init not enabled")  # pragma: no cover
