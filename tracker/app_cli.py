import click

from tracker import db
from tracker.coin_balances import coinbal_update
from tracker.prices import prices_update
from tracker.recurrent_update import recurrent_update
from tracker.tot_balances import tot_balances_update
from tracker.utils import exit_with_failure, valid_date, get_exception_str


def _template_to_title(template) -> str:
    column_names = [s.split(":")[0] for s in template.strip("{}").split("}{")]
    column_dict = {t: t for t in column_names}
    return template.format(**column_dict)


@click.command(name="setup_all")
def setup_all_cmd():
    """
    Setup the app (create db)
    """
    ok, res = db.general.create_tables()
    if ok:
        print("DB tables created successfully")
    else:
        print(f"ERROR: {res}")


# region coin


@click.group(name="coin")
def coin_cmd():
    """All regarding coins"""
    pass


@coin_cmd.command(name="add")
@click.argument("symbol", type=str)
@click.argument("name", type=str)
@click.argument("coingecko_id", type=str)
def coin_add_cmd(symbol: str, name: str, coingecko_id: str):
    """
    Add a coin to the db

    SYMBOL: coin_cmd symbol (es: BTC) \n
    NAME: coin_cmd name (es: Bitcoin) \n
    COINGECKO_ID: id of the coin_cmd on coingecko (es: bitcoin) \n
    """

    if not symbol or not name or not coingecko_id:
        exit_with_failure("Invalid input")

    try:
        db.coin.add(symbol, name, coingecko_id)
        click.echo("Coin added to the system")
    except Exception as e:
        exit_with_failure(f"ERROR: {get_exception_str(e)}")


@coin_cmd.command(name="list")
def coin_list_cmd():
    """
    List all coins.
    """

    coins = db.coin.select()

    template = "{ID:^8}" "{SYMBOL:^10}" "{NAME:^15}" "{COINGECKO_ID:^20}"
    click.echo("\n" + _template_to_title(template))
    for c in coins:
        click.echo(
            template.format(
                ID=f"{c['id']}",
                SYMBOL=f"{c['symbol']}",
                NAME=f"{c['name']}",
                COINGECKO_ID=f"{c['coingecko_id']}",
            )
        )


# endregion

# region deposit


@click.group(name="deposit")
def deposit_cmd():
    """All regarding deposits"""
    pass


@deposit_cmd.command(name="add")
@click.argument("symbol", type=str)
@click.argument("amount", type=float)
@click.argument("date", type=str)
def deposit_add_cmd(symbol: str, amount: float, date: str):
    """
    Add the deposit of coin_cmd to the db (transaction in)

    SYMBOL: coin_cmd symbol (es: BTC) \n
    AMOUNT: coin_cmd amount added (es: 0.03) \n
    DATE: date of the transaction (YYYY-MM-DD) \n
    """

    if len(symbol) == 0 or amount < 0 or not valid_date(date):
        exit_with_failure("Invalid input")

    coin_id = db.coin.get_id_by_symbol(symbol)
    assert coin_id, "Invalid coin"

    try:
        db.transaction.add_deposit(coin_id, amount, date)
        click.echo("Deposit added to the system")

    except Exception as e:
        exit_with_failure(f"ERROR: {get_exception_str(e)}")


@deposit_cmd.command(name="list")
def deposit_list_cmd():
    """
    List all deposits.
    """

    deposits = db.transaction.select_deposits()

    template = "{ID:^8}" "{COIN:^10}" "{AMOUNT:>12}" "{DATE:^20}"
    click.echo("\n" + _template_to_title(template))
    for d in deposits:
        coin_symbol = db.coin.get_symbol_by_id(d["coin_id"])
        click.echo(
            template.format(
                ID=f"{d['id']}",
                COIN=coin_symbol,
                AMOUNT=f"{d['amount']}",
                DATE=f"{d['date']}",
            )
        )


# endregion

# region withdrawal


@click.group(name="withdrawal")
def withdrawal_cmd():
    """All regarding withdrawals"""
    pass


@withdrawal_cmd.command(name="add")
@click.argument("symbol", type=str)
@click.argument("amount", type=float)
@click.argument("date", type=str)
def withdrawal_add_cmd(symbol: str, amount: float, date: str):
    """
    Add the withdraw of coin_cmd to the db (transaction out)

    SYMBOL: coin_cmd symbol (es: BTC) \n
    AMOUNT: coin_cmd amount removed (es: 0.03) \n
    DATE: date of the transaction (YYYY-MM-DD) \n
    """

    if len(symbol) == 0 or amount < 0 or not valid_date(date):
        exit_with_failure("Invalid input")

    coin_id = db.coin.get_id_by_symbol(symbol)
    assert coin_id, "Invalid coin"

    try:
        db.transaction.add_withdrawal(coin_id, amount, date)
        click.echo("Withdraw added to the system")

    except Exception as e:
        exit_with_failure(f"ERROR: {get_exception_str(e)}")


@withdrawal_cmd.command(name="list")
def withdrawal_list_cmd():
    """
    List all withdraws.
    """

    withdraws = db.transaction.select_withdrawals()

    template = "{ID:^8}" "{COIN:^10}" "{AMOUNT:>12}" "{DATE:^20}"
    click.echo("\n" + _template_to_title(template))
    for w in withdraws:
        coin_symbol = db.coin.get_symbol_by_id(w["coin_id"])
        click.echo(
            template.format(
                ID=f"{w['id']}",
                COIN=coin_symbol,
                AMOUNT=f"{w['amount']}",
                DATE=f"{w['date']}",
            )
        )


# endregion

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


@click.command(name="update_tot_balances")
def update_tot_balances():
    """
    Add the total balances of the portfolio (eur and usd) for all dates needed.
    To run after update_coin_balances and update_prices
    """
    tot_balances_update()


@click.command(name="update_all")
def update_all():
    """
    Do all updates necessary (coin_balances, prices and total_balances) and the updated graph.
    """
    recurrent_update()


# region balance


@click.group(name="balance")
def balance_cmd():
    """All regarding balances"""
    pass


@balance_cmd.command(name="list-last")
def balance_list_cmd():
    """
    List last coin balances.
    """

    coin_balances = db.balance.get_last_coin_balances()

    template = "{DATE:<16}" "{COIN:<10}" "{AMOUNT:<20}"
    click.echo("\n" + _template_to_title(template))
    for cb in coin_balances:
        click.echo(
            template.format(
                DATE=str(cb["date"]),
                COIN=db.coin.get_symbol_by_id(cb["coin_id"]),
                AMOUNT=cb["amount"],
            )
        )


# endregion
