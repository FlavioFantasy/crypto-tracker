from datetime import date
from typing import Optional, Union

from tracker.db.general import get_conn, tuple_rows_to_dict


def db_get_coin_balances(date: str = None):
    conn = get_conn()
    curr = conn.cursor()

    sql_select = """
        SELECT *
        FROM coin_balances
        {}
    """
    where_clause = f"WHERE date='{date}'" if date else ""

    curr.execute(sql_select.format(where_clause))
    res = curr.fetchall()

    conn.close()
    return tuple_rows_to_dict(res)


def db_get_tot_balances(
    date_: Optional[Union[str, date]] = None,
    start_date: Optional[Union[str, date]] = None,
    end_date: Optional[Union[str, date]] = None,
):
    conn = get_conn()
    curr = conn.cursor()

    sql_select = """
        SELECT *
        FROM tot_balances
        {}
    """

    where_clause = ""
    if date_:
        where_clause += " WHERE " if not where_clause else " AND "
        where_clause += f"date = '{date_}'"
    if start_date:
        where_clause += " WHERE " if not where_clause else " AND "
        where_clause += f"date >= '{start_date}'"
    if end_date:
        where_clause += " WHERE " if not where_clause else " AND "
        where_clause += f"date <= '{end_date}'"

    sql_select = sql_select.format(where_clause)

    curr.execute(sql_select)
    res = curr.fetchall()

    conn.close()
    return tuple_rows_to_dict(res)


def db_get_missing_tot_balances():
    conn = get_conn()
    curr = conn.cursor()

    sql_select = """
        SELECT CB.date, CB.amount, P.coin_eur, P.coin_usd
        FROM coin_balances as CB
        JOIN prices as P
            on CB.coin_id = P.coin_id and CB.date = P.date
        WHERE NOT EXISTS
            (SELECT *
            FROM tot_balances as TB
            WHERE TB.date = CB.date
            )
    """

    curr.execute(sql_select)
    res = curr.fetchall()

    conn.close()
    return tuple_rows_to_dict(res)


def db_add_coin_balance(date: str, coin_id: int, amount: float):
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = """
        INSERT INTO coin_balances (date, coin_id, amount)
        VALUES (?, ?, ?)
    """
    curr.execute(
        sql_insert,
        (
            date,
            coin_id,
            amount,
        ),
    )

    conn.commit()
    conn.close()


def db_add_tot_balance(date: str, eur_amount: float, usd_amount: float):
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = """
        INSERT INTO tot_balances (date, eur_amount, usd_amount)
        VALUES (?, ?, ?)
    """
    curr.execute(
        sql_insert,
        (
            date,
            eur_amount,
            usd_amount,
        ),
    )

    conn.commit()
    conn.close()
