# https://www.coingecko.com/en/api/documentation
# NOTE: max 50 requests per minute

import time
from datetime import date

import requests
from pycoingecko import CoinGeckoAPI  # type: ignore

from tracker.utils import EUR_FAKE_CG_ID

COINGECKO_MAX_WAIT_TIME = 61


class CoingeckoMaxWaitTimeError(Exception):
    pass


class CoinbaseUnexpectedError(Exception):
    pass


def cg_get_coin_price(date_: date, coin_type: str, coingecko_id: str) -> float:
    """Get the price of coin on specified date

    :return: coin_eur
    """
    # eur
    if coingecko_id == EUR_FAKE_CG_ID:
        return 1.00

    # other coins
    cg = CoinGeckoAPI()

    coin_eur = None
    t = 10
    while not coin_eur:
        try:
            coin_history = cg.get_coin_history_by_id(
                coingecko_id, date_.strftime("%d-%m-%Y")
            )
            coin_eur = coin_history["market_data"]["current_price"]["eur"]
        # exceded 50 reqs in a minute
        except (requests.exceptions.HTTPError, ValueError) as e:
            if t >= COINGECKO_MAX_WAIT_TIME:
                msg_e = f"Reached max waiting time ({t}s)"
                raise CoingeckoMaxWaitTimeError(msg_e)
            print(f"caught {e} ...")
            print(f"Waiting {t}s ...")
            time.sleep(t)
            t += 10

    msg_e = f"Failed to get {coin_type} price (in EUR) for {date_} with coingecko"
    assert coin_eur, msg_e
    return round(float(coin_eur), 2)
