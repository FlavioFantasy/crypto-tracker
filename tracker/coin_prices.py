import time

import requests

from tracker import db
from tracker.coingecko_api import *
from tracker.utils import log_info


def add_missing_coin_prices() -> None:
    """Add missing coin prices, after getting valuation for each day"""

    missing_coin_prices = get_missing_coin_prices()
    if missing_coin_prices:
        # save in db
        # for p in missing_coin_prices:
        #     db.price.add(p["date"], p["coin_id"], p["coin_usd"], p["coin_eur"])

        print("I WOULD ADD IN DB, BUT THIS IS TEST")

        msg = (
            f"added {len(missing_coin_prices)} rows to prices "
            f"(from {missing_coin_prices[0]['date']} to {missing_coin_prices[-1]['date']})"
        )
    else:
        msg = "no rows were added"

    log_info(f"add_missing_coin_prices: {msg}")


def get_missing_coin_prices() -> List[dict]:
    """Get missing coin prices, using CoinGecko APIs

    :return: [ {  }, ... ]
    """

    def elaborate_missing_prices(
        all_coins_: List[dict], missing_prices_: List[dict], prices_: List[dict]
    ) -> None:
        for mp_ in missing_prices_:
            coins_ = [c for c in all_coins_ if c["id"] == mp_["coin_id"]]
            date_ = mp_["date"]
            print(f"getting prices for {date_} - {coins_[0]['symbol']}")
            prices_date_ = cg_get_prices_by_date(coins_, date_)

            prices_ += prices_date_

    # get missing date-coin
    missing_prices = db.price.get_missing()
    print(f"missing_prices: {missing_prices}")

    coins = db.coin.select()

    coin_prices = []
    num_done = 0
    num_tot = len(missing_prices)

    # try untill it fails (max req in a minute)
    while num_done < num_tot:
        try:
            # do from what i have done
            elaborate_missing_prices(coins, missing_prices[num_done:], coin_prices)

            num_done = len(coin_prices)

        # exceded 50 reqs in a minute
        except (requests.exceptions.HTTPError, ValueError) as e:
            print(f"caught {e} ...")
            num_done = len(coin_prices)
            print(f" > Done {num_done} out of {num_tot}, waiting 62 secs ...")
            time.sleep(62)

    return coin_prices


add_missing_coin_prices()
