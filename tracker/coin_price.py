import time
from typing import List

import requests

from tracker import db
from tracker.external_api.coingecko_api import cg_get_coin_price
from tracker.utils import log_info, EUR_FAKE_CG_ID


def add_missing_coin_prices() -> None:
    """Add missing coin prices, after getting valuation for each day"""

    missing_coin_prices = get_missing_coin_prices()
    if missing_coin_prices:
        # save in db
        for cp in missing_coin_prices:
            db.price.add(cp["date"], cp["coin_id"], cp["coin_eur"])

        msg = (
            f"added {len(missing_coin_prices)} rows to prices "
            f"(from {missing_coin_prices[0]['date']} to {missing_coin_prices[-1]['date']})"
        )
    else:
        msg = "no rows were added"

    log_info(f"add_missing_coin_prices: {msg}")


def get_missing_coin_prices() -> List[dict]:
    """Get missing coin prices, using CoinGecko APIs

    :return: [ { date_, coin_id:_, coin_eur:_ }, ... ]
    """

    # get missing date-coin
    missing_prices = db.price.get_missing()
    # print(f"missing_prices: {missing_prices}")

    coin_id_to_coingecko_id = {c["id"]: c["coingecko_id"] for c in db.coin.select()}

    coin_prices: List[dict] = []

    # try untill it fails (max req in a minute)
    for mp in missing_prices:
        # print("\ndoing: ", mp)
        cp: dict = {}
        t = 10
        while not cp:
            try:
                coingecko_id = coin_id_to_coingecko_id[mp["coin_id"]]
                if coingecko_id == EUR_FAKE_CG_ID:
                    cp = {
                        "date": mp["date"],
                        "coin_id": mp["coin_id"],
                        "coin_eur": 1.00,
                    }
                else:
                    cp = cg_get_coin_price(mp["coin_id"], coingecko_id, mp["date"])
            # exceded 50 reqs in a minute
            except (requests.exceptions.HTTPError, ValueError) as e:
                # print(f"caught {e} ...")
                msg = f"Got {len(coin_prices)}/{len(missing_prices)} prices, waiting {t} secs ..."
                print(msg)
                time.sleep(t)
                t += 10
        coin_prices.append(cp)

    return coin_prices
