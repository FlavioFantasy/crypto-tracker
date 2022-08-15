import click

from tracker import db
from tracker.cli.utils import echo_success, echo_fail
from tracker.global_operation import add_all_missing, send_recaps


@click.command(name="init-db")
def setup_all_cmd():
    """
    Setup the app, creating sqlite db file and db tables
    """
    ok, res = db.general.create_tables()
    if ok:
        echo_success("DB tables created successfully")
    else:
        echo_fail(f"ERROR: {res}")


@click.command(name="monthly-update")
def monthly_update_cmd():
    """
    Add all missing data (coin_balances, prices and total_balances) and the eur graph and send Telegram messages
    """
    add_all_missing()
    send_recaps()
