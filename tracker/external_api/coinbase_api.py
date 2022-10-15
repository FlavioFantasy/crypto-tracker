from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Optional, Union

import requests

COINBASE_API = "https://api.coinbase.com/v2/"
ATTEMPTS = 3


class CoinbaseInvalidBaseCurrencyError(Exception):
    pass

class CoinbaseUnexpectedError(Exception):
    pass


def cb_get_coin_price(date_: Union[str, date], coin_type: str) -> Optional[Decimal]:
    """Get the price of coin on specified date

    :return: coin_eur
    """

    endpoint = f"prices/{coin_type}-EUR/spot?date={date_}"
    url = COINBASE_API + endpoint
    print("\n", url)
    # response = requests.get(url).json()
    # exch_rate = Decimal(response["data"]["amount"])

    coin_eur = None
    for _ in range(ATTEMPTS):
        try:
            response = requests.get(url).json()

            if "errors" in response:
                if "message" in response["errors"][0] and response["errors"][0]["message"] == "Invalid base currency":
                    raise CoinbaseInvalidBaseCurrencyError(f"Invalid base currency for CoinBase: {coin_type} (url={url}, response={response})")
                raise CoinbaseUnexpectedError(f"url={url}, response={response}")

            exch_rate = Decimal(response["data"]["amount"])

        except TimeoutError:
            continue

        if exch_rate != 0:
            coin_eur = exch_rate
            break

    return round(coin_eur, 2) if coin_eur else None
