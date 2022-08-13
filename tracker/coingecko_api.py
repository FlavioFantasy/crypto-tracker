# https://www.coingecko.com/en/api/documentation
# NOTE: max 50 requests per minute

import re
from typing import List

from pycoingecko import CoinGeckoAPI  # type: ignore


def cg_get_prices_by_date(coins: List[dict], date: str):
    """
    get the prices of all coins by the specified date

    :param coins: list of coins (from db table 'coins')
    :param date: date considered (YYYY-MM-DD)
    :return: list of datas to add to the db table 'prices'
    """

    # change date format from YYYY-MM-DD to DD-MM-YYYY
    date_rev = re.sub(r"(\d{4})-(\d{1,2})-(\d{1,2})", "\\3-\\2-\\1", date)

    cg = CoinGeckoAPI()

    # res
    crypto_data = []

    # print(f"cg date: {date}")
    # print(f"cg coins: {coins}")

    for coin in coins:
        coin_history = cg.get_coin_history_by_id(id=coin["coingecko_id"], date=date_rev)

        coin_usd = round(coin_history["market_data"]["current_price"]["usd"], 2)
        coin_eur = round(coin_history["market_data"]["current_price"]["eur"], 2)

        # add crypto data to add to db
        crypto_data.append(
            {
                "date": date,
                "coin_id": coin["id"],
                "coin_usd": coin_usd,
                "coin_eur": coin_eur,
            }
        )

        # global num_calls
        # num_calls += 1

    # print(f"crypto_data: {crypto_data}")
    return crypto_data


# if __name__ == "__main__":
#     pass
#     coins = [
#         {
#             "id": 3,
#             "symbol": "BETH",
#             "name": "BinanceETH",
#             "coingecko_id": "binance-eth",
#         },
#         {"id": 2, "symbol": "ETH", "name": "Ethereum", "coingecko_id": "ethereum"},
#     ]
#     x = cg_get_prices_by_date(coins, "01-11-2021")
#     print(x)
