from datetime import date
from typing import List, Optional, Union

from tracker.db.general import get_conn, tuple_rows_to_dict


def select(date_: Optional[Union[str, date]] = None) -> List[dict]:
    conn = get_conn()
    curr = conn.cursor()

    sql_select = """
        SELECT *
        FROM prices
        {}
    """
    where_clause = f"WHERE date='{date_}'" if date_ else ""

    curr.execute(sql_select.format(where_clause))
    res = curr.fetchall()

    conn.close()

    return tuple_rows_to_dict(res)


def get_missing() -> List[dict]:
    """ find which data are missing from the prices table, based on date and coin present in coin_balances """
    conn = get_conn()
    curr = conn.cursor()

    sql_select = """
        SELECT date, coin_id
        FROM coin_balances as CB
        WHERE NOT EXISTS (
            SELECT *
            FROM prices as P
            WHERE CB.date = P.date and CB.coin_id = P.coin_id
        )
    """

    curr.execute(sql_select)
    res = curr.fetchall()

    conn.close()

    return tuple_rows_to_dict(res)


def add(
    date_: Union[str, date], coin_id: int, coin_usd: float, coin_eur: float
) -> None:
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = """
        INSERT INTO prices (date, coin_id, coin_usd, coin_eur)
        VALUES (?, ?, ?, ?)
    """
    insert_params = [date_, coin_id, coin_usd, coin_eur]
    curr.execute(sql_insert, insert_params)

    conn.commit()
    conn.close()
