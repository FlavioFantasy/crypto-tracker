import click

from tracker import db
from tracker.cli.utils import template_to_title, TrackerClickGroup, echo_fail


@click.group(name="balance", cls=TrackerClickGroup)
def balance_cmd():
    """All regarding balances"""
    pass


@balance_cmd.command(name="list-coin-lasts")
def balance_list_coin_lasts_cmd():
    """
    List last coin balances
    """

    coin_balances = db.balance.get_last_coin_balances()

    template = "{DATE:<16}" "{COIN:<10}" "{AMOUNT:>16}"
    click.echo("\n" + template_to_title(template))
    for cb in coin_balances:
        click.echo(
            template.format(
                DATE=str(cb["date"]),
                COIN=db.coin.get_symbol_by_id(cb["coin_id"]),
                AMOUNT=round(cb["amount"], 8),
            )
        )


@balance_cmd.command(name="list-tot-by-date")
@click.argument("date", type=str)
def balance_list_tot_by_date_cmd(date: str):
    """
    List total (EUR) balance by date
    """

    tot_balance = db.balance.get_tot_balances(date)

    if not tot_balance:
        echo_fail(f"No available total balance for {date}")
    else:
        tot_eur = f"{tot_balance[0]['eur_amount']:.2f}"
        click.echo(f"Total balance for {date}: {tot_eur} EUR")
