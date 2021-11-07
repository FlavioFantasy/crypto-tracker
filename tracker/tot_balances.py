import copy
from datetime import datetime, timedelta
from typing import List

from tracker import utils
from tracker.db_handler import *
# from tracker.coingecko_api import *
import re
import operator
import itertools

def tot_balances_get():

    missing_tot_bals = db_get_missing_tot_balances()

    # group missing total balances by date
    grouped_missing = []
    missing_tot_bals = sorted(missing_tot_bals, key=operator.itemgetter("date"))
    for i, g in itertools.groupby(missing_tot_bals, key=operator.itemgetter("date")):
        grouped_missing.append(list(g))

    # print(f"grouped:")
    # print(json.dumps(grouped_missing, indent=2, default=str))

    # calculate total balances
    tot_bals = []
    for date_group in grouped_missing:
        # print(f"date_group: {date_group}")
        date_bal = {
            "date": date_group[0]["date"],
            "eur_amount": 0.0,
            "usd_amount": 0.0
        }
        for entry in date_group:
            date_bal["eur_amount"] += entry["amount"] * entry["coin_eur"]
            date_bal["usd_amount"] += entry["amount"] * entry["coin_usd"]
        tot_bals.append(date_bal)

    # for b in tot_bals:
    #     print(f"tb: {b}")
    # print()

    return tot_bals


def tot_balances_save_on_db(tot_balances: List[dict]):
    for b in tot_balances:
        db_add_tot_balance(b["date"], b["eur_amount"], b["usd_amount"])


def tot_balances_update():
    tot_balances = tot_balances_get()
    if len(tot_balances) > 0:
        tot_balances_save_on_db(tot_balances)
        str_to_show = f"tot_balances_update: saved {len(tot_balances)} tot_bal on db (from {tot_balances[0]['date']} to {tot_balances[-1]['date']})"
    else:
        str_to_show = "tot_balances_update: no update were made"

    utils.log_info(str_to_show)
    print(str_to_show)


# if __name__ == '__main__':
#     tot_balances_update()


