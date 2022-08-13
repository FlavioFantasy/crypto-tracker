import click

from tracker import db
from tracker.cli.utils import _template_to_title, TrackerClickGroup


@click.group(name="balance", cls=TrackerClickGroup)
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
