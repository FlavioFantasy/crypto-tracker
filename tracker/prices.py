import time

import requests

from tracker import db
from tracker import utils
from tracker.coingecko_api import *


def prices_get():
    def elaborate_missing_prices(
        all_coins_: List[dict], missing_prices_: List[dict], prices_: List[dict]
    ) -> None:
        for mp_ in missing_prices_:
            coins_ = [c for c in all_coins_ if c["id"] == mp_["coin_id"]]
            date_ = mp_["date"]
            print(f"getting prices for {date_} - {coins_[0]['symbol']}")
            prices_date_ = cg_get_prices_by_date(coins_, date_)

            prices_ += prices_date_

    # find which data are missing from the prices table, based on date and coin present in coin_balances
    missing_prices = db.price.get_missing()
    # print(f"missing_prices: {missing_prices}")
    all_coins = db.coin.select()

    prices = []
    num_done = 0
    num_tot = len(missing_prices)

    # try untill it fails (max req in a minute)
    while num_done < num_tot:
        try:
            # do from what i have done
            elaborate_missing_prices(all_coins, missing_prices[num_done:], prices)

            num_done = len(prices)

        # exceded 50 reqs in a minute
        except (requests.exceptions.HTTPError, ValueError) as e:
            print(f"caught {e} ...")
            num_done = len(prices)
            print(f" > Done {num_done} out of {num_tot}, waiting 62 secs ...")
            time.sleep(62)

    # feedback
    # for p in prices:
    #     print(f"p: {p}")
    # print()

    return prices


def prices_save_on_db(prices: List[dict]):
    for p in prices:
        db.price.add(p["date"], p["coin_id"], p["coin_usd"], p["coin_eur"])


def prices_update():
    prices = prices_get()
    if len(prices) > 0:
        prices_save_on_db(prices)
        str_to_show = f"prices_update: saved {len(prices)} prices on db (from {prices[0]['date']} to {prices[-1]['date']})"
    else:
        str_to_show = "prices_update: no update were made"

    utils.log_info(str_to_show)
    print(str_to_show)


# if __name__ == '__main__':
#     prices_update()
