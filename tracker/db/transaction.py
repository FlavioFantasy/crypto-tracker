from typing import List

from tracker.db.general import get_conn, tuple_rows_to_dict


def select_deposits(date: str = None) -> List[dict]:
    conn = get_conn()
    curr = conn.cursor()

    sql_select = """
        SELECT *
        FROM deposits
        {}
        ORDER BY date
    """
    where_clause = f"WHERE date='{date}'" if date else ""

    curr.execute(sql_select.format(where_clause))
    res = curr.fetchall()

    conn.close()
    return tuple_rows_to_dict(res)


def add_deposit(coin_id: int, amount: float, date: str) -> None:
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = """
        INSERT INTO deposits (coin_id, amount, date)
        VALUES (?, ?, ?)
    """
    insert_params = [coin_id, amount, date]
    curr.execute(sql_insert, insert_params)

    conn.commit()
    conn.close()


def select_withdrawals(date: str = None) -> List[dict]:
    conn = get_conn()
    curr = conn.cursor()

    sql_select = """
        SELECT *
        FROM withdraws
        {}
        ORDER BY date
    """
    where_clause = f"WHERE date='{date}'" if date else ""

    curr.execute(sql_select.format(where_clause))
    res = curr.fetchall()

    conn.close()
    return tuple_rows_to_dict(res)


def add_withdrawal(coin_id: int, amount: float, date: str) -> None:
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = """
        INSERT INTO withdraws (coin_id, amount, date)
        VALUES (?, ?, ?)
    """
    insert_params = [coin_id, amount, date]
    curr.execute(sql_insert, insert_params)

    conn.commit()
    conn.close()


def get_all_transactions() -> List[dict]:
    # get transactions and categorize them

    all_deposits = select_deposits()
    all_deposits = [dict(d, action="in") for d in all_deposits]

    all_withdraws = select_withdrawals()
    all_withdraws = [dict(w, action="out") for w in all_withdraws]

    all_transactions = all_deposits + all_withdraws
    all_transactions = sorted(all_transactions, key=lambda d: d["date"])

    return all_transactions
