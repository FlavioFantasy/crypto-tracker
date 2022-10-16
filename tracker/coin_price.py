from typing import List

from tracker import db
from tracker.external_api.coinbase_api import (
    cb_get_coin_price,
    CoinbaseInvalidBaseCurrencyError,
)
from tracker.external_api.coingecko_api import cg_get_coin_price
from tracker.utils import log_info


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

    :return: [ { date_, coin_id:_, coin_ticker:_, coin_eur:_ }, ... ]
    """

    # get missing date-coin
    missing_prices = db.price.get_missing()
    # print(f"missing_prices: {missing_prices}")

    coin_id_to_coingecko_id = {c["id"]: c["coingecko_id"] for c in db.coin.select()}
    coin_id_to_ticker = {c["id"]: c["symbol"] for c in db.coin.select()}

    coin_prices: List[dict] = []

    # try untill it fails (max req in a minute)
    for mp in missing_prices:
        # print("\ndoing: ", mp)
        date_ = mp["date"]
        coin_ticker = coin_id_to_ticker[mp["coin_id"]]
        coingecko_id = coin_id_to_coingecko_id[mp["coin_id"]]
        try:
            coin_eur = cb_get_coin_price(date_, coin_ticker)
        except CoinbaseInvalidBaseCurrencyError as e:
            # print(f"Handling exc ({e}) using Coingecko APIs...")
            coin_eur = cg_get_coin_price(date_, coin_ticker, coingecko_id)

        cp = {
            "date": date_,
            "coin_id": mp["coin_id"],
            "coin_ticker": coin_ticker,
            "coin_eur": coin_eur,
        }
        # print(f"cp: {cp}")
        coin_prices.append(cp)

    return coin_prices
