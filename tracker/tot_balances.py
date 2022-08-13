import itertools
import operator
from typing import List

from tracker import db
from tracker import utils
from tracker.telegram_handler import send_message


def tot_balances_get():

    missing_tot_bals = db.balance.get_missing_tot_balances()

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
        date_bal = {"date": date_group[0]["date"], "eur_amount": 0.0, "usd_amount": 0.0}
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
        db.balance.add_tot_balance(b["date"], b["eur_amount"], b["usd_amount"])


def get_day_details(date: str) -> str:
    # details
    num_coins = {c["coin_id"]: c["amount"] for c in db.balance.get_coin_balances(date)}
    val_coins = {c["coin_id"]: c["coin_eur"] for c in db.price.db_get_prices(date)}

    tot_eur = 0
    last_day_amts = []
    for c in num_coins:
        eur_amt = num_coins[c] * val_coins[c]
        last_day_amts.append(
            {"coin_id": c, "eur_amount": eur_amt, "coin_amount": num_coins[c]}
        )
        tot_eur += eur_amt

    for c in last_day_amts:
        c["percentage"] = c["eur_amount"] / tot_eur
        c["coin_name"] = db.coin.db_get_coin_symbol_by_id(c["coin_id"])

    # order by relevance
    last_day_amts = sorted(last_day_amts, key=lambda d: d["percentage"], reverse=True)

    return f"{date} asset allocation:\n" + "\n".join(
        [
            f" - {c['coin_name']:<5}: {round(c['eur_amount'], 2):>7.2f}€ ({round(c['percentage'] * 100, 2):05.2f}%)  - {round(c['coin_amount'], 8)}"
            for c in last_day_amts
        ]
    )


def tot_balances_update():
    tot_balances = tot_balances_get()
    if len(tot_balances) > 0:
        tot_balances_save_on_db(tot_balances)
        str_to_show = f"tot_balances_update: saved {len(tot_balances)} tot_bal on db (from {tot_balances[0]['date']} to {tot_balances[-1]['date']})"
        str_to_send = f"Balance updated on {tot_balances[-1]['date']}: {round(tot_balances[-1]['eur_amount'], 2)} €"
    else:
        str_to_show = "tot_balances_update: no update were made"
        str_to_send = f"No balances were added"

    utils.log_info(str_to_show)

    print(str_to_show)
    send_message(str_to_send)

    send_message(get_day_details(tot_balances[-1]["date"]))


# if __name__ == "__main__":
#     send_message(get_day_details("2022-03-31"))
