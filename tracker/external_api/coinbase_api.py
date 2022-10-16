from datetime import date
from decimal import Decimal
from typing import Union

import requests

from tracker.utils import EUR_TICKER

COINBASE_API = "https://api.coinbase.com/v2/"
ATTEMPTS = 3


class CoinbaseInvalidBaseCurrencyError(Exception):
    pass


class CoinbaseUnexpectedError(Exception):
    pass


def cb_get_coin_price(date_: Union[str, date], coin_type: str) -> float:
    """Get the price of coin on specified date

    :return: coin_eur
    """
    # eur
    if coin_type == EUR_TICKER:
        return 1.00

    # other coins
    endpoint = f"prices/{coin_type}-EUR/spot?date={date_}"
    url = COINBASE_API + endpoint

    coin_eur = None
    for _ in range(ATTEMPTS):
        try:
            response = requests.get(url).json()

            if "errors" in response:
                if (
                    "message" in response["errors"][0]
                    and response["errors"][0]["message"] == "Invalid base currency"
                ):
                    raise CoinbaseInvalidBaseCurrencyError(
                        f"Invalid base currency for CoinBase: {coin_type} (url={url}, response={response})"
                    )
                raise CoinbaseUnexpectedError(f"url={url}, response={response}")

            exch_rate = Decimal(response["data"]["amount"])

        except TimeoutError:
            continue

        if exch_rate != 0:
            coin_eur = exch_rate
            break

    msg_e = f"Failed to get {coin_type} price (in EUR) for {date_} with coinbase"
    assert coin_eur, msg_e
    return round(float(coin_eur), 2)
