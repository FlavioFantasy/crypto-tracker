from datetime import date
from typing import List, Dict

from tracker import db
from tracker.telegram_handler import send_message
from tracker.utils import log_info


def add_missing_total_balances() -> None:
    """Add missing total balances, after calculating eur and usd amount for each day"""

    missing_total_balances = calculate_missing_total_balances()
    if missing_total_balances:
        # save in db
        for tb in missing_total_balances:
            db.balance.add_tot_balance(tb["date"], tb["eur_amount"], tb["usd_amount"])

        msg = (
            f"added {len(missing_total_balances)} rows to tot_balances "
            f"(from {missing_total_balances[0]['date']} to {missing_total_balances[-1]['date']})"
        )

        str_to_send = f"Balance updated on {missing_total_balances[-1]['date']}: {round(missing_total_balances[-1]['eur_amount'], 2)} €"
        send_message(str_to_send)  # TODO: move to different module
    else:
        msg = "no rows were added"

    log_info(f"add_missing_total_balances: {msg}")

    # send recap allocation  # TODO: move to different module
    send_message(get_day_details(missing_total_balances[-1]["date"]))


def calculate_missing_total_balances() -> List[dict]:
    """Calculate missing daily balances (value), ordered by date

    :return: [ { date:_, eur_amount:_, usd_amount:_ }, ... ]
    """

    missing_total_balances = db.balance.get_missing_tot_balances()
    # print("missing_tot_bals: ", missing_total_balances)

    # group by date
    missing_total_balances_by_date: Dict[date, list] = {}
    for mb in missing_total_balances:
        if mb["date"] not in missing_total_balances_by_date:
            missing_total_balances_by_date[mb["date"]] = []
        missing_total_balances_by_date[mb["date"]].append(mb)

    # calculate total balances
    total_balances: List[dict] = []
    for d, coins_dets in missing_total_balances_by_date.items():
        daily_bal = {
            "date": d,
            "eur_amount": sum(c["amount"] * c["coin_eur"] for c in coins_dets),
            "usd_amount": sum(c["amount"] * c["coin_usd"] for c in coins_dets),
        }
        # print("daily_bal: ", daily_bal)
        total_balances.append(daily_bal)

    return total_balances


def get_day_details(date: str) -> str:
    # details
    num_coins = {c["coin_id"]: c["amount"] for c in db.balance.get_coin_balances(date)}
    val_coins = {c["coin_id"]: c["coin_eur"] for c in db.price.select(date)}

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
        c["coin_name"] = db.coin.get_symbol_by_id(c["coin_id"])

    # order by relevance
    last_day_amts = sorted(last_day_amts, key=lambda d: d["percentage"], reverse=True)

    return f"{date} asset allocation:\n" + "\n".join(
        [
            f" - {c['coin_name']:<5}: {round(c['eur_amount'], 2):>7.2f}€ ({round(c['percentage'] * 100, 2):05.2f}%)  - {round(c['coin_amount'], 8)}"
            for c in last_day_amts
        ]
    )
