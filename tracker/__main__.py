from .app_cli import *


@click.group()
def crypto_tracker() -> None:
    """
    Set of commands to handle the db app
    """
    pass  # pragma: no cover


crypto_tracker.add_command(setup_all_cmd)

crypto_tracker.add_command(coin_cmd)
crypto_tracker.add_command(deposit_cmd)
crypto_tracker.add_command(withdrawal_cmd)

crypto_tracker.add_command(update_coin_balances)
crypto_tracker.add_command(update_prices)
crypto_tracker.add_command(update_tot_balances)
crypto_tracker.add_command(update_all)
