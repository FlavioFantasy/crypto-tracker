from datetime import date
from typing import List, Optional, Union

from tracker.db.general import get_conn, tuple_rows_to_dict


def select_deposits(date_: Optional[Union[str, date]] = None) -> List[dict]:
    conn = get_conn()
    curr = conn.cursor()

    sql_select = """
        SELECT *
        FROM deposits
        {}
        ORDER BY date
    """
    where_clause = f"WHERE date='{date_}'" if date_ else ""

    curr.execute(sql_select.format(where_clause))
    res = curr.fetchall()

    conn.close()
    return tuple_rows_to_dict(res)


def add_deposit(coin_id: int, amount: float, date_: Union[str, date]) -> None:
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = """
        INSERT INTO deposits (coin_id, amount, date)
        VALUES (?, ?, ?)
    """
    insert_params = [coin_id, amount, date_]
    curr.execute(sql_insert, insert_params)

    conn.commit()
    conn.close()


def select_withdrawals(date_: Optional[Union[str, date]] = None) -> List[dict]:
    conn = get_conn()
    curr = conn.cursor()

    sql_select = """
        SELECT *
        FROM withdraws
        {}
        ORDER BY date
    """
    where_clause = f"WHERE date='{date_}'" if date_ else ""

    curr.execute(sql_select.format(where_clause))
    res = curr.fetchall()

    conn.close()
    return tuple_rows_to_dict(res)


def add_withdrawal(coin_id: int, amount: float, date_: Union[str, date]) -> None:
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = """
        INSERT INTO withdraws (coin_id, amount, date)
        VALUES (?, ?, ?)
    """
    insert_params = [coin_id, amount, date_]
    curr.execute(sql_insert, insert_params)

    conn.commit()
    conn.close()


def get_transactions() -> List[dict]:
    """Get transactions (deposits and withdrawals), ordered by date

    :return: [ {id:_, coin_id:_, amount:_, date:_, action:in/out}, ... ]
    """
    deposits = [{**d, "action": "in"} for d in select_deposits()]
    withdraws = [{**w, "action": "out"} for w in select_withdrawals()]

    transactions = sorted(deposits + withdraws, key=lambda d: d["date"])
    return transactions
