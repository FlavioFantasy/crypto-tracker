from tracker.db.general import get_conn, tuple_rows_to_dict


def db_get_prices(date: str = None):
    conn = get_conn()
    curr = conn.cursor()

    sql_select = """
        SELECT *
        FROM prices
        {}
    """
    where_clause = f"WHERE date='{date}'" if date else ""

    curr.execute(sql_select.format(where_clause))
    res = curr.fetchall()

    conn.close()
    return tuple_rows_to_dict(res)


def db_get_missing_prices():
    conn = get_conn()
    curr = conn.cursor()

    sql_select = """
        SELECT date, coin_id
        FROM coin_balances as CB
        WHERE NOT EXISTS
            (SELECT *
             FROM prices as P
             WHERE CB.date = P.date and CB.coin_id = P.coin_id
        )
    """

    curr.execute(sql_select)
    res = curr.fetchall()

    conn.close()
    return tuple_rows_to_dict(res)


def db_add_price(date: str, coin_id: int, coin_usd: float, coin_eur: float):
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = """
        INSERT INTO prices (date, coin_id, coin_usd, coin_eur)
        VALUES (?, ?, ?, ?)
    """
    curr.execute(
        sql_insert,
        (
            date,
            coin_id,
            coin_usd,
            coin_eur,
        ),
    )

    conn.commit()
    conn.close()
