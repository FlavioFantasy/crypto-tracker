import re
from datetime import datetime

from tracker.config import CurrentConf


def log_info(msg: str) -> None:

    today_str = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
    log_file = CurrentConf.get().get_log_file()

    with open(log_file, "a") as f:
        f.write(f"[INFO] {today_str} - {msg} \n")


def log_error(msg: str) -> None:

    today_str = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
    log_file = CurrentConf.get().get_log_file()

    with open(log_file, "a") as f:
        f.write(f"[ERROR] {today_str} - {msg} \n")


def valid_date(date: str) -> bool:
    return re.fullmatch("[0-9]{4}-([01])[0-9]-[0-3][0-9]", date) is not None


def get_exception_str(e: BaseException) -> str:
    return f"{type(e).__name__} - {e}"
