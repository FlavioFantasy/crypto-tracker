from datetime import date
from typing import Optional, Union, List

from tracker.db.general import get_conn, tuple_rows_to_dict


# region coin-balances


def get_coin_balances(date_: Optional[Union[str, date]] = None) -> List[dict]:
    conn = get_conn()
    curr = conn.cursor()

    sql_select = """
        SELECT *
        FROM coin_balances
        {}
    """
    where_clause = f"WHERE date='{date_}'" if date_ else ""
    sql_select = sql_select.format(where_clause)

    curr.execute(sql_select)
    res = curr.fetchall()

    conn.close()

    return tuple_rows_to_dict(res)


def add_coin_balance(date_: Union[str, date], coin_id: int, amount: float) -> None:
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = """
        INSERT INTO coin_balances (date, coin_id, amount)
        VALUES (?, ?, ?)
    """
    insert_params = [date_, coin_id, amount]

    curr.execute(sql_insert, insert_params)
    conn.commit()

    conn.close()


def get_last_coin_balances() -> List[dict]:
    conn = get_conn()
    curr = conn.cursor()

    sql_select = """
        SELECT * 
        FROM coin_balances
        WHERE date = (
            SELECT date
            FROM coin_balances
            ORDER BY date DESC 
            LIMIT 1
        )
    """

    curr.execute(sql_select)
    res = curr.fetchall()

    conn.close()

    return tuple_rows_to_dict(res)


# endregion

# region tot-balances (eur)


def get_tot_balances(
    date_: Optional[Union[str, date]] = None,
    start_date: Optional[Union[str, date]] = None,
    end_date: Optional[Union[str, date]] = None,
) -> List[dict]:
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


def get_missing_tot_balances() -> List[dict]:
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


def add_tot_balance(
    date_: Union[str, date], eur_amount: float, usd_amount: float
) -> None:
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = """
        INSERT INTO tot_balances (date, eur_amount, usd_amount)
        VALUES (?, ?, ?)
    """

    insert_params = [date_, eur_amount, usd_amount]
    curr.execute(sql_insert, insert_params)

    conn.commit()
    conn.close()


# endregion
