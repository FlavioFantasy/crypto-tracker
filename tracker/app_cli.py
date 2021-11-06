import copy
from datetime import datetime, timedelta

import click

from tracker import db_handler, coingecko_api
from tracker.utils import exit_with_failure, valid_date
from tracker.db_handler import *
from tracker.coin_balances import coinbal_update
from tracker.prices import prices_update

# add ---------------------------------------------------------------------------------------------

@click.command(name="add_coin")
@click.argument("symbol", type=str)
@click.argument("name", type=str)
@click.argument("coingecko_id", type=str)
def add_coin(symbol: str, name: str, coingecko_id: str):
    """
    Add a coin to the db

    SYMBOL: coin symbol (es: BTC) \n
    NAME: coin name (es: Bitcoin) \n
    COINGECKO_ID: id of the coin on coingecko (es: bitcoin) \n
    """

    if len(symbol) == 0 or len(name) == 0 or len(coingecko_id) == 0:
        exit_with_failure("Invalid input")

    try:
        db_add_coin(symbol, name, coingecko_id)
        click.echo("Coin added to the system")
    except Exception as e:
        exit_with_failure(f"ERROR: {str(e)}")

@click.command(name="add_deposit")
@click.argument("symbol", type=str)
@click.argument("amount", type=float)
@click.argument("date", type=str)
def add_deposit(symbol: str, amount: float, date: str):
    """
    Add the deposit of coin to the db (transaction in)

    SYMBOL: coin symbol (es: BTC) \n
    AMOUNT: coin amount added (es: 0.03) \n
    DATE: date of the transaction (YYYY-MM-DD) \n
    """

    if len(symbol) == 0 or amount < 0 or not valid_date(date):
        exit_with_failure("Invalid input")

    coin_id = db_get_coin_id_by_symbol(symbol)
    if coin_id is None:
        exit_with_failure("Invalid symbol")

    try:
        db_add_deposit(coin_id, amount, date)
        click.echo("Deposit added to the system")

    except Exception as e:
        exit_with_failure(f"ERROR: {type(e).__name__} - {str(e)}")

@click.command(name="add_withdraw")
@click.argument("symbol", type=str)
@click.argument("amount", type=float)
@click.argument("date", type=str)
def add_withdraw(symbol: str, amount: float, date: str):
    """
    Add the withdraw of coin to the db (transaction out)

    SYMBOL: coin symbol (es: BTC) \n
    AMOUNT: coin amount removed (es: 0.03) \n
    DATE: date of the transaction (YYYY-MM-DD) \n
    """

    if len(symbol) == 0 or amount < 0 or not valid_date(date):
        exit_with_failure("Invalid input")

    coin_id = db_get_coin_id_by_symbol(symbol)
    if coin_id is None:
        exit_with_failure("Invalid symbol")

    try:
        db_add_withdraws(coin_id, amount, date)
        click.echo("Withdraw added to the system")

    except Exception as e:
        exit_with_failure(f"ERROR: {type(e).__name__} - {str(e)}")

# view --------------------------------------------------------------------------------------------

@click.command(name="list_coins")
def list_coins():
    """
    List all coins.
    """

    template = (
        "{ID:^8}"
        "{SYMBOL:^10}"
        "{NAME:^15}"
        "{COINGECKO_ID:^20}"
    )
    click.echo(
        "\n"
        + template.format(
            ID="ID",
            SYMBOL="SYMBOL",
            NAME="NAME",
            COINGECKO_ID="COINGECKO_ID",
        )
    )

    coins = db_get_coins()

    for c in coins:
        click.echo(
            template.format(
                ID=f"{c['id']}",
                SYMBOL=f"{c['symbol']}",
                NAME=f"{c['name']}",
                COINGECKO_ID=f"{c['coingecko_id']}",
            )
        )

@click.command(name="list_deposits")
def list_deposits():
    """
    List all deposits.
    """

    template = (
        "{ID:^8}"
        "{COIN:^10}"
        "{AMOUNT:>12}"
        "{DATE:^20}"
    )
    click.echo(
        "\n"
        + template.format(
            ID="ID",
            COIN="COIN",
            AMOUNT="AMOUNT",
            DATE="DATE",
        )
    )

    deposits = db_get_deposits()

    for d in deposits:
        coin_symbol = db_get_coin_symbol_by_id(d["coin_id"])
        click.echo(
            template.format(
                ID=f"{d['id']}",
                COIN=coin_symbol,
                AMOUNT=f"{d['amount']}",
                DATE=f"{d['date']}",
            )
        )

@click.command(name="list_withdraws")
def list_withdraws():
    """
    List all withdraws.
    """

    template = (
        "{ID:^8}"
        "{COIN:^10}"
        "{AMOUNT:>12}"
        "{DATE:^20}"
    )
    click.echo(
        "\n"
        + template.format(
            ID="ID",
            COIN="COIN",
            AMOUNT="AMOUNT",
            DATE="DATE",
        )
    )

    withdraws = db_get_withdraws()

    for w in withdraws:
        coin_symbol = db_get_coin_symbol_by_id(w["coin_id"])
        click.echo(
            template.format(
                ID=f"{w['id']}",
                COIN=coin_symbol,
                AMOUNT=f"{w['amount']}",
                DATE=f"{w['date']}",
            )
        )

# periodic updates --------------------------------------------------------------------------------

@click.command(name="update_coin_balances")
def update_coin_balances():
    """
    Add the coin balances in the db if needed (based on all deposit and withdraws)
    """

    coinbal_update()


@click.command(name="update_prices")
def update_prices():
    """
    Add the coins price for each date in the db if needed (i have that coin in that date).
    To run after update_coin_balances
    """

    prices_update()
