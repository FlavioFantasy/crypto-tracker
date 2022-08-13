import re
from datetime import datetime

from tracker.config import CurrentConf


def log_info(msg: str) -> None:
    with open(CurrentConf.get().get_log_file(), "a") as f:
        f.write(f"[INFO] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg} \n")


def log_error(msg: str) -> None:
    with open(CurrentConf.get().get_log_file(), "a") as f:
        f.write(f"[ERROR] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg} \n")


def valid_date(date: str) -> bool:
    return re.fullmatch("[0-9]{4}-([01])[0-9]-[0-3][0-9]", date) is not None


def get_exception_str(e: BaseException) -> str:
    return f"{type(e).__name__} - {e}"
