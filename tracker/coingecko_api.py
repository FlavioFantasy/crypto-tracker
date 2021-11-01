
# https://www.coingecko.com/en/api/documentation
# NOTE: max 50 requests per minute
from typing import List

from pycoingecko import CoinGeckoAPI
import datetime, calendar
import time


def cg_get_prices_by_date(coins: List[dict], date: str):
    """
    get the prices of all coins by the specified date

    :param coins: list of coins (from db table 'coins')
    :param date: date considered
    :return: list of datas to add to the db table 'prices'
    """

    cg = CoinGeckoAPI()

    # res
    crypto_data = []

    for coin in coins:
        coin_history = cg.get_coin_history_by_id(id=coin["coingecko_id"], date=date)

        coin_usd = round(coin_history["market_data"]["current_price"]["usd"], 2)
        coin_eur = round(coin_history["market_data"]["current_price"]["eur"], 2)

        # add crypto data to add to db
        crypto_data.append({
            "date": date,
            "coin_id": coin["id"],
            "coin_usd": coin_usd,
            "coin_eur": coin_eur
        })

        # global num_calls
        # num_calls += 1

    return crypto_data


# if __name__ == '__main__':
#     pass
#     coins = [
#         {
#             "id": 1,
#             "symbol": "BTC",
#             "name": "Bitcoin",
#             "coingecko_id": "bitcoin"
#         },
#         {
#             "id": 2,
#             "symbol": "ETH",
#             "name": "Ethereum",
#             "coingecko_id": "ethereum"
#         }
#     ]
#     x = cg_get_prices_by_date(coins, "01-11-2021")
