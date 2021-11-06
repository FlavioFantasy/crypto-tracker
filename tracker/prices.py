import copy
from datetime import datetime, timedelta
from typing import List

from tracker import utils
from tracker.db_handler import *
import coingecko_api
import re

def prices_get():
    # find which data are missing from the prices table, based on date and coin present in coin_balances
    missing_prices = db_get_missing_prices()
    print(f"missing_prices: {missing_prices}")
    all_coins = db_get_coins()

    todo_prices = []
    for mp in missing_prices:
        coins = [c for c in all_coins if c["id"] == mp["coin_id"]]
        date = mp["date"]
        prices = cg_get_prices_by_date(coins, date)
        todo_prices += prices

    for p in todo_prices:
        print(f"p: {p}")
    print()

    return todo_prices


def prices_save_on_db(prices: List[dict]):
    for p in prices:
        db_add_price(p["date"], p["coin_id"], p["coin_usd"], p["coin_eur"])


def prices_update():
    prices = prices_get()
    if len(prices) > 0:
        prices_save_on_db(prices)
        str_to_show = f"prices_update: saved {len(prices)} prices on db (from {prices[0]['date']} to {prices[-1]['date']})"
    else:
        str_to_show = "prices_update: no update were made"

    utils.log_info(str_to_show)
    print(str_to_show)


if __name__ == '__main__':
    prices_update()


