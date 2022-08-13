import click

from tracker import db
from tracker.recurrent_update import recurrent_update


@click.command(name="setup-all")
def setup_all_cmd():
    """
    Setup the app (create db)
    """
    ok, res = db.general.create_tables()
    if ok:
        print("DB tables created successfully")
    else:
        print(f"ERROR: {res}")


@click.command(name="update-all")
def update_all_cmd():
    """
    Do all recurrent updates necessary (coin_balances, prices and total_balances) and the updated graph.
    """
    recurrent_update()
