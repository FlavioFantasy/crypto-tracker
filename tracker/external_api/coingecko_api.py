# https://www.coingecko.com/en/api/documentation
# NOTE: max 50 requests per minute

from datetime import date

from pycoingecko import CoinGeckoAPI  # type: ignore

cg = CoinGeckoAPI()


def cg_get_coin_price(coin_id: int, coingecko_id: str, date_: date) -> dict:
    """Get the price of coin on specified date

    :return: { date:_, coin_id:_, coin_eur:_ }
    """

    coin_history = cg.get_coin_history_by_id(
        id=coingecko_id, date=date_.strftime("%d-%m-%Y")
    )

    return {
        "date": date_,
        "coin_id": coin_id,
        "coin_eur": round(coin_history["market_data"]["current_price"]["eur"], 2),
    }
