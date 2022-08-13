import click

from tracker import db
from tracker.cli.utils import echo_success, echo_fail
from tracker.recurrent_update import recurrent_update


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


@click.command(name="update-all")
def update_all_cmd():
    """
    Do all recurrent updates necessary (coin_balances, prices and total_balances) and the updated graph.
    """
    recurrent_update()
