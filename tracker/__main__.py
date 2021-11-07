import click

from .app_cli import *


@click.group()
def crypto_tracker() -> None:
    """
    Set of commands to handle the db app
    """
    pass  # pragma: no cover


crypto_tracker.add_command(add_coin)
crypto_tracker.add_command(add_deposit)
crypto_tracker.add_command(add_withdraw)

crypto_tracker.add_command(list_coins)
crypto_tracker.add_command(list_deposits)
crypto_tracker.add_command(list_withdraws)

crypto_tracker.add_command(update_coin_balances)
crypto_tracker.add_command(update_prices)
crypto_tracker.add_command(update_tot_balances)
crypto_tracker.add_command(update_all)
