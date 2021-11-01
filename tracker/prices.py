import copy
from datetime import datetime, timedelta
from typing import List

from tracker import utils
from tracker.db_handler import db_get_all_transactions, db_add_coin_balance, db_get_coin_balances, db_get_prices


def prices_get():
    coin_bals = db_get_coin_balances()

    # get all dates
    start_date_str = coin_bals[0]["date"]
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    today = datetime.today().date()

    all_dates = [(start_date + timedelta(days=x)).strftime("%Y-%m-%d") for x in range((today - start_date).days)]

    # already done
    prices = db_get_prices()
    done_dates = [p["date"] for p in prices]
    done_dates = list(dict.fromkeys(done_dates))

    todo_dates = [d for d in all_dates if d not in done_dates]

    # todo: from here

    balances = []

    # calculate balances for the dates i need
    for date in todo_dates:
        date_bal = {
            "date": date
        }

        to_remove = []

        # calculate balances for transactions we are considering
        yesterday_coins = balances[-1]["coins"] if len(balances) > 0 else []
        date_coins = copy.deepcopy(yesterday_coins)

        for t in [tx for tx in all_transactions if tx["date"] == date]:

            # add if coin not in list
            if t["coin_id"] not in [c["coin_id"] for c in date_coins]:
                date_coins.append({
                    "coin_id": t["coin_id"],
                    "amount": 0
                })

            # get coin ref
            coin_ref = next((item for item in date_coins if item["coin_id"] == t["coin_id"]), None)

            # in or out
            if t["action"] == "in":
                coin_ref["amount"] += t["amount"]
            else:
                coin_ref["amount"] -= t["amount"]

                if coin_ref["amount"] == 0:
                    to_remove.append(t["coin_id"])

        # cleanup
        for c_rem in to_remove:
            date_coins = [c for c in date_coins if c["coin_id"] != c_rem]

        date_bal["coins"] = date_coins

        # append to all
        # print(date_bal)
        balances.append(date_bal)

    for b in balances:
        print(f"bal: {b}")
    return balances


def prices_save_on_db(balances: List[dict]):
    for b in balances:
        for c in b["coins"]:
            db_add_coin_balance(b["date"], c["coin_id"], c["amount"])


def prices_update():
    prices = prices_get()
    prices_save_on_db(prices)

    str_to_show = f"saved {len(balances)} coin balances on db (from {balances[0]['date']} to {balances[-1]['date']})"
    utils.log_info(str_to_show)
    print(str_to_show)
