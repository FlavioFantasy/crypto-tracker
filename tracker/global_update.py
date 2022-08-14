from datetime import date

from dateutil.relativedelta import relativedelta

from tracker.coin_balance import add_missing_coin_balances
from tracker.coin_price import add_missing_coin_prices
from tracker.graph_drawer import draw_and_send
from tracker.total_balance import add_missing_total_balances


def add_all_missing():
    """Add all missing data (coin balances, prices and total balances) and draw eur graph"""

    add_missing_coin_balances()
    add_missing_coin_prices()
    add_missing_total_balances()

    # all
    draw_and_send()
    # last month
    s = date.today() - relativedelta(months=1)
    draw_and_send(s)


if __name__ == "__main__":
    add_all_missing()
