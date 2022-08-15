import glob
from datetime import date

from dateutil.relativedelta import relativedelta

from tracker import db
from tracker.coin_balance import add_missing_coin_balances
from tracker.coin_price import add_missing_coin_prices
from tracker.config import CurrentConf
from tracker.external_api.telegram_api import tg_send_message, tg_send_image
from tracker.graph_drawer import draw_save_graph
from tracker.total_balance import add_missing_total_balances, get_asset_allocation
from tracker.utils import log_info


def add_all_missing() -> None:
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


def send_recaps() -> None:
    """Send Telegram messages with recap of asset allocation and graphs"""

    last_tot_bal_date = db.balance.get_tot_balances(get_only_last=True)[0]["date"]

    # asset allocation
    asset_allocation = get_asset_allocation(last_tot_bal_date)
    msg = (
        f"Asset allocation on {asset_allocation['date']}:\n"
        + "\n".join(
            [
                f" - {c['ticker']:<5}: {c['eur_amt']:>7.2f}€ ({c['percentage'] * 100:05.2f}%) - {c['coin_amt']}"
                for c in asset_allocation["coins"]
            ]
        )
        + f"\n\nTotal: {asset_allocation['tot_eur']}€"
    )
    tg_send_message(msg)

    # eur graphs
    imgs_folder = CurrentConf.get().get_imgs_folder()
    this_month_graphs = [
        f_path
        for f_path in glob.glob(f"{imgs_folder}*.png")
        if f"{last_tot_bal_date.year}{last_tot_bal_date.month:02}" in f_path
    ]
    for img_path in this_month_graphs:
        tg_send_image(img_path)

    log_info(f"send_recaps: sent Telegram messages")
