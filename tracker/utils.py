import re
import sys
from datetime import datetime


import click

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


def build_error(error, env_name: str = None) -> dict:
    return {"env_name": env_name, "error": error}


def build_result(res, env_name: str = None) -> dict:
    return {"env_name": env_name, "res": res}


def exit_with_failure(msg: str, new_line: bool = True) -> None:
    click.echo(click.style(msg, fg="red"), nl=new_line)
    sys.exit(1)


def valid_date(date: str) -> bool:
    return re.fullmatch("[0-9]{4}-([01])[0-9]-[0-3][0-9]", date) is not None
