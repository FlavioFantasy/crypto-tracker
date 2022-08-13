import copy
from datetime import datetime, timedelta
from typing import List

from tracker import db
from tracker.utils import log_info


def add_missing_coin_balances() -> None:
    """
    Add missing coin balances, after calculating coin amount for each day
    """

    missing_coin_balances = calculate_missing_coin_balances()
    if missing_coin_balances:
        # save in db
        for cb in missing_coin_balances:
            for c in cb["coins"]:
                db.balance.add_coin_balance(cb["date"], c["coin_id"], c["amount"])

        msg = (
            f"added {len(missing_coin_balances)} rows to coin_balances "
            f"(from {missing_coin_balances[0]['date']} to {missing_coin_balances[-1]['date']})"
        )
    else:
        msg = "no rows were added"

    log_info(f"add_missing_coin_balances: {msg}")


def calculate_missing_coin_balances() -> List[dict]:
    """Calculate missing daily balances for each coin, ordered by date

    :return: [ { date:_, coins: [ { coin_id:_, amount:_ }, ... ] }, ... ]
    """

    # get current coin balances
    coin_bals = db.balance.get_coin_balances()

    # get all txs (in and out)
    transactions = db.transaction.get_transactions()

    # get all dates, from 1st tx to yesterday
    all_dates = [
        (transactions[0]["date"] + timedelta(days=x))
        for x in range((datetime.today().date() - transactions[0]["date"]).days)
    ]

    # get to do dates
    done_dates = list(set(b["date"] for b in coin_bals))
    todo_dates = [d for d in all_dates if d not in done_dates]

    # track daily balances
    daily_balances: List[dict] = []

    # if present, add last day coin balances
    if coin_bals:
        last_day_cbs = [cb for cb in coin_bals if cb["date"] == coin_bals[-1]["date"]]
        last_daily_bal = {
            "date": last_day_cbs[0]["date"],
            "coins": [
                {"coin_id": i["coin_id"], "amount": i["amount"]} for i in last_day_cbs
            ],
        }
        # print("last_daily_bal: ", last_daily_bal)
        daily_balances.append(last_daily_bal)

    # calculate balances for the dates I need
    for d in todo_dates:
        # print("d: ", d)

        prev_day_coins = daily_balances[-1]["coins"] if daily_balances else []
        curr_day_coins = copy.deepcopy(prev_day_coins)
        # print("curr_day_coins: ", curr_day_coins)

        # for each tx (dep, wit) done in the date I am looping
        for t in [tx for tx in transactions if tx["date"] == d]:
            # print("t: ", t)

            # I didnt have that coin the previous day
            if t["coin_id"] not in [c["coin_id"] for c in curr_day_coins]:
                # add with amt=0, since it will be updated later
                curr_day_coins.append({"coin_id": t["coin_id"], "amount": 0})

            # get reference to dict, to easily update its value
            coin_ref = next(c for c in curr_day_coins if c["coin_id"] == t["coin_id"])

            # update coin balance
            amt_to_add = t["amount"] if t["action"] == "in" else -t["amount"]
            coin_ref["amount"] += amt_to_add
            # print("curr_day_coins: ", curr_day_coins)

        # remove if amount is zero
        curr_day_coins = [c for c in curr_day_coins if c["amount"] != 0]

        daily_bal = {"date": d, "coins": curr_day_coins}
        # print("daily_bal: ", daily_bal)

        daily_balances.append(daily_bal)
        # print()

    # remove first daily balance if date was already in db
    if db.balance.get_coin_balances(date_=daily_balances[0]["date"]):
        daily_balances.pop(0)

    return daily_balances
