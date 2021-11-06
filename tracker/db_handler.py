import json
import sqlite3
from sqlite3.dbapi2 import connect
from typing import Dict, List, Tuple
from tracker.config import CurrentConf
from tracker.coingecko_api import cg_get_prices_by_date

# general -----------------------------------------------------------------------------------------

def tuple_rows_to_dict(rows: List[Tuple]) -> List[Dict]:
    result = []
    for row in rows:
        result.append(dict(row))

    return result

def get_conn():
    db_file = CurrentConf.get().get_db_file()

    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row

    return conn

def db_create_tables():
    try:
        conn = get_conn()
        curr = conn.cursor()

        sql_create = '''
            CREATE TABLE coins (
                id INTEGER PRIMARY KEY,
                symbol TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                coingecko_id TEXT NOT NULL
            )
        '''
        curr.execute(sql_create)

        sql_create = '''
            CREATE TABLE prices (
                date DATE NOT NULL,
                coin_id INTEGER NOT NULL,
                coin_usd NUMERIC NOT NULL,
                coin_eur NUMERIC NOT NULL,

                PRIMARY KEY (date, coin_id),
                FOREIGN KEY (coin_id)
                    REFERENCES coins (id)
            )
        '''
        curr.execute(sql_create)

        sql_create = '''
            CREATE TABLE coin_balances (
                date DATE NOT NULL,
                coin_id INTEGER NOT NULL,
                amount NUMERIC NOT NULL,

                PRIMARY KEY (date, coin_id),
                FOREIGN KEY (coin_id)
                    REFERENCES coins (id)
            )
        '''
        curr.execute(sql_create)

        sql_create = '''
            CREATE TABLE deposits (
                id INTEGER PRIMARY KEY,
                coin_id INTEGER NOT NULL,
                amount NUMERIC NOT NULL,
                date DATE NOT NULL,

                FOREIGN KEY (coin_id)
                    REFERENCES coins (id)
            )
        '''
        curr.execute(sql_create)

        sql_create = '''
            CREATE TABLE withdraws (
                id INTEGER PRIMARY KEY,
                coin_id INTEGER NOT NULL,
                amount NUMERIC NOT NULL,
                date DATE NOT NULL,

                FOREIGN KEY (coin_id)
                    REFERENCES coins (id)
            )
        '''
        curr.execute(sql_create)

        sql_create = '''
            CREATE TABLE tot_balances (
                date DATE NOT NULL PRIMARY KEY,
                eur_amount NUMERIC NOT NULL,
                usd_amount NUMERIC NOT NULL
            )
        '''
        curr.execute(sql_create)

        conn.commit()
        conn.close()
        return True, "ok"

    except Exception as e:
        return False, f"{type(e).__name__} - {e}"

# select ------------------------------------------------------------------------------------------

def db_get_coin_id_by_symbol(symbol: str) -> int:
    conn = get_conn()
    curr = conn.cursor()

    sql_select = '''
        SELECT id
        FROM coins
        {}
    '''
    where_clause = f"WHERE symbol='{symbol}'"

    curr.execute(sql_select.format(where_clause))
    res = curr.fetchone()

    conn.close()
    return res["id"] if res else None


def db_get_coin_symbol_by_id(coin_id: int) -> str:
    conn = get_conn()
    curr = conn.cursor()

    sql_select = '''
        SELECT symbol
        FROM coins
        {}
    '''
    where_clause = f"WHERE id='{coin_id}'"

    curr.execute(sql_select.format(where_clause))
    res = curr.fetchone()

    conn.close()
    return res["symbol"] if res else None

def db_get_coins():
    conn = get_conn()
    curr = conn.cursor()

    sql_select = '''
        SELECT *
        FROM coins
    '''

    curr.execute(sql_select)
    res = curr.fetchall()

    conn.close()
    return tuple_rows_to_dict(res)

def db_get_prices(date: str = None):
    conn = get_conn()
    curr = conn.cursor()

    sql_select = '''
        SELECT *
        FROM prices
        {}
    '''
    where_clause = f"WHERE date='{date}'" if date else ""

    curr.execute(sql_select.format(where_clause))
    res = curr.fetchall()

    conn.close()
    return tuple_rows_to_dict(res)

def db_get_deposits(date: str = None):
    conn = get_conn()
    curr = conn.cursor()

    sql_select = '''
        SELECT *
        FROM deposits
        {}
        ORDER BY date
    '''
    where_clause = f"WHERE date='{date}'" if date else ""

    curr.execute(sql_select.format(where_clause))
    res = curr.fetchall()

    conn.close()
    return tuple_rows_to_dict(res)

def db_get_withdraws(date: str = None):
    conn = get_conn()
    curr = conn.cursor()

    sql_select = '''
        SELECT *
        FROM withdraws
        {}
        ORDER BY date
    '''
    where_clause = f"WHERE date='{date}'" if date else ""

    curr.execute(sql_select.format(where_clause))
    res = curr.fetchall()

    conn.close()
    return tuple_rows_to_dict(res)

def db_get_coin_balances(date: str = None):
    conn = get_conn()
    curr = conn.cursor()

    sql_select = '''
        SELECT *
        FROM coin_balances
        {}
    '''
    where_clause = f"WHERE date='{date}'" if date else ""

    curr.execute(sql_select.format(where_clause))
    res = curr.fetchall()

    conn.close()
    return tuple_rows_to_dict(res)

def db_get_tot_balances(date: str = None):
    conn = get_conn()
    curr = conn.cursor()

    sql_select = '''
        SELECT *
        FROM tot_balances
        {}
    '''
    where_clause = f"WHERE date='{date}'" if date else ""

    curr.execute(sql_select.format(where_clause))
    res = curr.fetchall()

    conn.close()
    return tuple_rows_to_dict(res)

def db_get_all_transactions():
    # get transactions and categorize them

    all_deposits = db_get_deposits()
    all_deposits = [dict(d, action="in") for d in all_deposits]

    all_withdraws = db_get_withdraws()
    all_withdraws = [dict(w, action="out") for w in all_withdraws]

    all_transactions = all_deposits + all_withdraws
    all_transactions = sorted(all_transactions, key=lambda d: d["date"])

    return all_transactions


def db_get_missing_prices():
    conn = get_conn()
    curr = conn.cursor()

    sql_select = '''
        SELECT date, coin_id
        FROM coin_balances as CB
        WHERE NOT EXISTS
            (SELECT *
             FROM prices as P
             WHERE CB.date = P.date and CB.coin_id = P.coin_id
        )
    '''

    curr.execute(sql_select)
    res = curr.fetchall()

    conn.close()
    return tuple_rows_to_dict(res)

def db_get_missing_tot_balances():
    conn = get_conn()
    curr = conn.cursor()

    sql_select = '''
        SELECT CB.date, CB.amount, P.coin_eur, P.coin_usd
        FROM coin_balances as CB
        JOIN prices as P
            on CB.coin_id = P.coin_id and CB.date = P.date
        WHERE NOT EXISTS
            (SELECT *
            FROM tot_balances as TB
            WHERE TB.date = CB.date
            )
    '''

    curr.execute(sql_select)
    res = curr.fetchall()

    conn.close()
    return tuple_rows_to_dict(res)

# insert ------------------------------------------------------------------------------------------

def db_add_coin(symbol: str, name: str, coingecko_id: str):
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = '''
        INSERT INTO coins (symbol, name, coingecko_id)
        VALUES (?, ?, ?)
    '''
    curr.execute(sql_insert, (symbol, name, coingecko_id, ))

    conn.commit()
    conn.close()

def db_add_price(date: str, coin_id: int, coin_usd: float, coin_eur: float):
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = '''
        INSERT INTO prices (date, coin_id, coin_usd, coin_eur)
        VALUES (?, ?, ?, ?)
    '''
    curr.execute(sql_insert, (date, coin_id, coin_usd, coin_eur, ))

    conn.commit()
    conn.close()

def db_add_deposit(coin_id: int, amount: float, date: str):
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = '''
        INSERT INTO deposits (coin_id, amount, date)
        VALUES (?, ?, ?)
    '''
    curr.execute(sql_insert, (coin_id, amount, date, ))

    conn.commit()
    conn.close()

def db_add_withdraws(coin_id: int, amount: float, date: str):
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = '''
        INSERT INTO withdraws (coin_id, amount, date)
        VALUES (?, ?, ?)
    '''
    curr.execute(sql_insert, (coin_id, amount, date, ))

    conn.commit()
    conn.close()

def db_add_coin_balance(date: str, coin_id: int, amount: float):
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = '''
        INSERT INTO coin_balances (date, coin_id, amount)
        VALUES (?, ?, ?)
    '''
    curr.execute(sql_insert, (date, coin_id, amount, ))

    conn.commit()
    conn.close()

def db_add_tot_balance(date: str, eur_amount: float, usd_amount: float):
    conn = get_conn()
    curr = conn.cursor()

    sql_insert = '''
        INSERT INTO tot_balances (date, eur_amount, usd_amount)
        VALUES (?, ?, ?)
    '''
    curr.execute(sql_insert, (date, eur_amount, usd_amount, ))

    conn.commit()
    conn.close()

# setup ------------------------------------------------------------------------------------------

def prepare_db():
    db_create_tables()

    db_add_coin("BTC", "Bitcoin", "bitcoin")
    db_add_coin("ETH", "Ethereum", "ethereum")


if __name__ == '__main__':
    pass

    # print(prepare_db())

    # print(db_get_coins())
    # print(db_get_prices())
    # print()
    #
    # # print(db_add_coin("BTC", "Bitcoin", "bitcoin"))
    # # print(db_add_coin("ETH", "Ethereum", "ethereum"))
    #
    # x = cg_get_prices_by_date(db_get_coins(), "31-10-2021")
    # print(x)
    # for c in x:
    #     db_add_price(c["date"], c["coin_id"], c["coin_usd"], c["coin_eur"])
    # print()
    #
    # print(db_get_coins())
    # print(db_get_prices())
    # print()

    print(db_get_coin_id_by_symbol("a"))
