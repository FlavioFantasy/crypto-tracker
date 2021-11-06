import copy
from datetime import datetime, timedelta
from typing import List

from tracker import utils
from tracker.db_handler import *
import coingecko_api
import re

def tot_balances_get():

    missing_tot_bals = db_get_missing_tot_balances()

    tot_bals = []
    # TODO : from here
    # find a way to group tot_bals to calculate for date, so that i can easy do the math on totals
    for b in missing_tot_bals:
        print(b)

    for b in tot_bals:
        print(f"b: {b}")
    print()

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


if __name__ == '__main__':
    tot_balances_get()
    # tot_balances_update()


