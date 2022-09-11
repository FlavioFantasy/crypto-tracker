from datetime import date
from typing import List, Dict

from tracker import db
from tracker.utils import log_info


def add_missing_total_balances() -> None:
    """Add missing total balances, after calculating eur and usd amount for each day"""

    missing_total_balances = calculate_missing_total_balances()
    if missing_total_balances:
        # save in db
        for tb in missing_total_balances:
            db.balance.add_tot_balance(tb["date"], tb["eur_amount"])

        msg = (
            f"added {len(missing_total_balances)} rows to tot_balances "
            f"(from {missing_total_balances[0]['date']} to {missing_total_balances[-1]['date']})"
        )
    else:
        msg = "no rows were added"

    log_info(f"add_missing_total_balances: {msg}")


def calculate_missing_total_balances() -> List[dict]:
    """Calculate missing daily balances (value), ordered by date

    :return: [ { date:_, eur_amount:_ }, ... ]
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
        }
        # print("daily_bal: ", daily_bal)
        total_balances.append(daily_bal)

    return total_balances


def get_asset_allocation(date_: date) -> dict:
    """Get portfolio allocation for specified date

    :return: { date:_, tot_eur:_, coins: [ ticker:_, eur_amt:_, coin_amt:_, percentage:_ ] }
    """

    coin_amt_by_id = {
        c["coin_id"]: c["amount"] for c in db.balance.get_coin_balances(date_)
    }
    coin_eur_by_id = {c["coin_id"]: c["coin_eur"] for c in db.price.select(date_)}

    tot_eur = 0
    coin_details = []
    for c_id, c_amt in coin_amt_by_id.items():
        eur_amt = round(coin_amt_by_id[c_id] * coin_eur_by_id[c_id], 2)
        coin_details.append(
            {
                "ticker": db.coin.get_symbol_by_id(c_id),
                "eur_amt": eur_amt,
                "coin_amt": round(c_amt, 8),
            }
        )
        tot_eur += eur_amt
    for c in coin_details:
        c["percentage"] = round(c["eur_amt"] / tot_eur, 4)

    # order by relevance
    coin_details = sorted(coin_details, key=lambda d: d["percentage"], reverse=True)

    return {"date": date_, "tot_eur": round(tot_eur, 2), "coins": coin_details}
