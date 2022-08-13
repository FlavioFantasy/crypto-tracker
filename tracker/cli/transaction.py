import click

from tracker import db
from tracker.cli.utils import _template_to_title
from tracker.utils import valid_date, exit_with_failure, get_exception_str


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
