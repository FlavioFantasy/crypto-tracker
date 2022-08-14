from datetime import date

from dateutil.relativedelta import relativedelta

from tracker.coin_balance import add_missing_coin_balances
from tracker.coin_price import add_missing_coin_prices
from tracker.graph_drawer import draw_save_graph
from tracker.total_balance import add_missing_total_balances


def add_all_missing():
    """Add all missing data (coin balances, prices and total balances) and draw eur graphs"""

    # add missing data in db
    add_missing_coin_balances()
    add_missing_coin_prices()
    add_missing_total_balances()

    # draw and save imgs
    fst_day_this_month = date.today().replace(day=1)
    fst_day_last_month = fst_day_this_month - relativedelta(months=1)

    draw_save_graph(end_date=fst_day_this_month)
    draw_save_graph(start_date=fst_day_last_month, end_date=fst_day_this_month)


def send_recaps():
    """Send Telegram messages with recap of asset allocation and graphs"""

    pass


if __name__ == "__main__":
    add_all_missing()
