import sqlite3
from sqlite3 import Connection
from typing import Dict, List, Tuple

from tracker.config import CurrentConf
from tracker.utils import get_exception_str


def tuple_rows_to_dict(rows: List[Tuple]) -> List[Dict]:
    result = []
    for row in rows:
        result.append(dict(row))

    return result


def get_conn() -> Connection:
    db_file = CurrentConf.get().get_db_file()

    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row

    return conn


def create_tables() -> Tuple[bool, str]:
    """Create all tables needed to use the app"""

    sql_create_coins = """
        CREATE TABLE coins (
            id INTEGER PRIMARY KEY,
            symbol TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            coingecko_id TEXT NOT NULL
        )
    """
    sql_create_deposits = """
        CREATE TABLE deposits (
            id INTEGER PRIMARY KEY,
            coin_id INTEGER NOT NULL,
            amount NUMERIC NOT NULL,
            date DATE NOT NULL,

            FOREIGN KEY (coin_id)
                REFERENCES coins (id)
        )
    """
    sql_create_withdraws = """
        CREATE TABLE withdraws (
            id INTEGER PRIMARY KEY,
            coin_id INTEGER NOT NULL,
            amount NUMERIC NOT NULL,
            date DATE NOT NULL,

            FOREIGN KEY (coin_id)
                REFERENCES coins (id)
        )
    """
    sql_create_prices = """
        CREATE TABLE prices (
            date DATE NOT NULL,
            coin_id INTEGER NOT NULL,
            coin_usd NUMERIC NOT NULL,
            coin_eur NUMERIC NOT NULL,

            PRIMARY KEY (date, coin_id),
            FOREIGN KEY (coin_id)
                REFERENCES coins (id)
        )
    """
    sql_create_coin_balance = """
        CREATE TABLE coin_balances (
            date DATE NOT NULL,
            coin_id INTEGER NOT NULL,
            amount NUMERIC NOT NULL,

            PRIMARY KEY (date, coin_id),
            FOREIGN KEY (coin_id)
                REFERENCES coins (id)
        )
    """
    sql_create_tot_balances = """
        CREATE TABLE tot_balances (
            date DATE NOT NULL PRIMARY KEY,
            eur_amount NUMERIC NOT NULL,
            usd_amount NUMERIC NOT NULL
        )
    """

    try:
        conn = get_conn()
        curr = conn.cursor()

        # create all tables
        curr.execute(sql_create_coins)

        curr.execute(sql_create_deposits)
        curr.execute(sql_create_withdraws)

        curr.execute(sql_create_prices)

        curr.execute(sql_create_coin_balance)
        curr.execute(sql_create_tot_balances)

        conn.commit()
        conn.close()

        return True, "ok"

    except Exception as e:
        return False, get_exception_str(e)
