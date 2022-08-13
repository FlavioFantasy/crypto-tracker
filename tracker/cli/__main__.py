import click

from tracker.cli.balance import balance_cmd
from tracker.cli.coin import coin_cmd
from tracker.cli.misc import setup_all_cmd, update_all_cmd
from tracker.cli.transaction import deposit_cmd, withdrawal_cmd
from tracker.cli.utils import TrackerClickGroup


@click.group(cls=TrackerClickGroup)
def crypto_tracker() -> None:
    """
    Set of commands to handle the db app
    """
    pass


crypto_tracker.add_command(coin_cmd)
crypto_tracker.add_command(deposit_cmd)
crypto_tracker.add_command(withdrawal_cmd)
crypto_tracker.add_command(balance_cmd)

crypto_tracker.add_command(setup_all_cmd)
crypto_tracker.add_command(update_all_cmd)
