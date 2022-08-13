import click

from tracker import db
from tracker.cli.utils import template_to_title, TrackerClickGroup, exit_with_failure
from tracker.utils import get_exception_str


@click.group(name="coin", cls=TrackerClickGroup)
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
    click.echo("\n" + template_to_title(template))
    for c in coins:
        click.echo(
            template.format(
                ID=f"{c['id']}",
                SYMBOL=f"{c['symbol']}",
                NAME=f"{c['name']}",
                COINGECKO_ID=f"{c['coingecko_id']}",
            )
        )
