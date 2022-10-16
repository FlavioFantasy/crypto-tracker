from typing import Optional, List

from tracker.db.general import get_conn, tuple_rows_to_dict


def get_id_by_symbol(symbol: str) -> Optional[int]:
    conn = get_conn()
    curr = conn.cursor()

    sql_select = """
        SELECT id
        FROM coins
        {}
    """
    where_clause = f"WHERE symbol='{symbol}'"
    sql_select = sql_select.format(where_clause)

    curr.execute(sql_select)
    res = curr.fetchone()

    conn.close()

    return res["id"] if res else None


def get_symbol_by_id(coin_id: int) -> Optional[str]:
    conn = get_conn()
    curr = conn.cursor()

    sql_select = """
        SELECT symbol
        FROM coins
        {}
    """
    where_clause = f"WHERE id='{coin_id}'"

    curr.execute(sql_select.format(where_clause))
    res = curr.fetchone()

    conn.close()

    return res["symbol"] if res else None


def select() -> List[dict]:
    """:return: [ {  } ]"""
    conn = get_conn()
    curr = conn.cursor()

    sql_select = """
        SELECT *
        FROM coins
    """

    curr.execute(sql_select)
    res = curr.fetchall()

    conn.close()

    return tuple_rows_to_dict(res)


def add(symbol: str, name: str, coingecko_id: str):
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = """
        INSERT INTO coins (symbol, name, coingecko_id)
        VALUES (?, ?, ?)
    """

    insert_params = [symbol, name, coingecko_id]
    curr.execute(sql_insert, insert_params)

    conn.commit()
    conn.close()
