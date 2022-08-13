import click

from tracker import db
from tracker.cli.utils import (
    template_to_title,
    TrackerClickGroup,
    exit_with_failure,
    echo_success,
)
from tracker.utils import valid_date, get_exception_str


@click.group(name="deposit", cls=TrackerClickGroup)
def deposit_cmd():
    """All regarding deposits"""
    pass


@deposit_cmd.command(name="add")
@click.argument("symbol", type=str)
@click.argument("amount", type=float)
@click.argument("date", type=str)
def deposit_add_cmd(symbol: str, amount: float, date: str):
    """
    Register the deposit of a coin (transaction in)

    SYMBOL: coin symbol (es: BTC) \n
    AMOUNT: coin amount added (es: 0.03) \n
    DATE: date of the transaction (YYYY-MM-DD) \n
    """

    if not symbol or amount < 0 or not valid_date(date):
        exit_with_failure("Invalid input")

    coin_id = db.coin.get_id_by_symbol(symbol)
    if not coin_id:
        exit_with_failure(f"Coin {symbol} not supported")
    assert coin_id

    try:
        db.transaction.add_deposit(coin_id, amount, date)
        echo_success("Deposit added to the system")
    except Exception as e:
        exit_with_failure(f"ERROR: {get_exception_str(e)}")


@deposit_cmd.command(name="list")
def deposit_list_cmd():
    """
    List all deposits
    """

    deposits = db.transaction.select_deposits()

    template = "{ID:<8}" "{DATE:<16}" "{COIN:<10}" "{AMOUNT:>16}"
    click.echo("\n" + template_to_title(template))
    for d in deposits:
        click.echo(
            template.format(
                ID=d["id"],
                DATE=str(d["date"]),
                COIN=db.coin.get_symbol_by_id(d["coin_id"]),
                AMOUNT=round(d["amount"], 8),
            )
        )


@click.group(name="withdrawal", cls=TrackerClickGroup)
def withdrawal_cmd():
    """All regarding withdrawals"""
    pass


@withdrawal_cmd.command(name="add")
@click.argument("symbol", type=str)
@click.argument("amount", type=float)
@click.argument("date", type=str)
def withdrawal_add_cmd(symbol: str, amount: float, date: str):
    """
    Register the withrawal of a coin (transaction out)

    SYMBOL: coin symbol (es: BTC) \n
    AMOUNT: coin amount removed (es: 0.03) \n
    DATE: date of the transaction (YYYY-MM-DD) \n
    """

    if not symbol or amount < 0 or not valid_date(date):
        exit_with_failure("Invalid input")

    coin_id = db.coin.get_id_by_symbol(symbol)
    if not coin_id:
        exit_with_failure(f"Coin {symbol} not supported")
    assert coin_id

    try:
        db.transaction.add_withdrawal(coin_id, amount, date)
        echo_success("Withdrawal added to the system")
    except Exception as e:
        exit_with_failure(f"ERROR: {get_exception_str(e)}")


@withdrawal_cmd.command(name="list")
def withdrawal_list_cmd():
    """
    List all withdraws.
    """

    withdraws = db.transaction.select_withdrawals()

    template = "{ID:<8}" "{DATE:<16}" "{COIN:<10}" "{AMOUNT:>16}"
    click.echo("\n" + template_to_title(template))
    for w in withdraws:
        click.echo(
            template.format(
                ID=w["id"],
                DATE=str(w["date"]),
                COIN=db.coin.get_symbol_by_id(w["coin_id"]),
                AMOUNT=round(w["amount"], 8),
            )
        )
