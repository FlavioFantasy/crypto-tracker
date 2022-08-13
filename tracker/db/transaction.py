from tracker.db.general import get_conn, tuple_rows_to_dict


def db_get_deposits(date: str = None):
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


def db_add_deposit(coin_id: int, amount: float, date: str):
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = """
        INSERT INTO deposits (coin_id, amount, date)
        VALUES (?, ?, ?)
    """
    curr.execute(
        sql_insert,
        (
            coin_id,
            amount,
            date,
        ),
    )

    conn.commit()
    conn.close()


def db_get_withdraws(date: str = None):
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


def db_add_withdraws(coin_id: int, amount: float, date: str):
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = """
        INSERT INTO withdraws (coin_id, amount, date)
        VALUES (?, ?, ?)
    """
    curr.execute(
        sql_insert,
        (
            coin_id,
            amount,
            date,
        ),
    )

    conn.commit()
    conn.close()


def db_get_all_transactions():
    # get transactions and categorize them

    all_deposits = db_get_deposits()
    all_deposits = [dict(d, action="in") for d in all_deposits]

    all_withdraws = db_get_withdraws()
    all_withdraws = [dict(w, action="out") for w in all_withdraws]

    all_transactions = all_deposits + all_withdraws
    all_transactions = sorted(all_transactions, key=lambda d: d["date"])

    return all_transactions
