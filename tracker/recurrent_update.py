from datetime import date

from dateutil.relativedelta import relativedelta

from tracker.coin_balances import add_missing_coin_balances
from tracker.graph_drawer import draw_and_send
from tracker.coin_prices import add_missing_coin_prices
from tracker.tot_balances import tot_balances_update


def recurrent_update():
    """
    Do all updates necessary (coin_balances, prices and total_balances) and the updated graph.
    """
    add_missing_coin_balances()
    add_missing_coin_prices()
    tot_balances_update()

    # all
    draw_and_send()
    # last month
    s = date.today() - relativedelta(months=1)
    draw_and_send(s)


if __name__ == "__main__":
    recurrent_update()
