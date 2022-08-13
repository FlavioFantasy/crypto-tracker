import re
from datetime import datetime

from tracker.config import CurrentConf


def log_info(msg: str) -> None:
    s = f"[INFO] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg} \n"
    with open(CurrentConf.get().get_log_file(), "a") as f:
        f.write(s)
    print(s)


def log_error(msg: str) -> None:
    s = f"[ERROR] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg} \n"
    with open(CurrentConf.get().get_log_file(), "a") as f:
        f.write(s)
    print(s)


def valid_date(date: str) -> bool:
    return re.fullmatch("[0-9]{4}-([01])[0-9]-[0-3][0-9]", date) is not None


def get_exception_str(e: BaseException) -> str:
    return f"{type(e).__name__} - {e}"
