import sqlite3
from sqlite3 import Connection
from typing import Dict, List, Tuple

from tracker.config import CurrentConf


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


def db_create_tables() -> Tuple[bool, str]:
    try:
        conn = get_conn()
        curr = conn.cursor()

        sql_create = """
            CREATE TABLE coins (
                id INTEGER PRIMARY KEY,
                symbol TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                coingecko_id TEXT NOT NULL
            )
        """
        curr.execute(sql_create)

        sql_create = """
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
        curr.execute(sql_create)

        sql_create = """
            CREATE TABLE coin_balances (
                date DATE NOT NULL,
                coin_id INTEGER NOT NULL,
                amount NUMERIC NOT NULL,

                PRIMARY KEY (date, coin_id),
                FOREIGN KEY (coin_id)
                    REFERENCES coins (id)
            )
        """
        curr.execute(sql_create)

        sql_create = """
            CREATE TABLE deposits (
                id INTEGER PRIMARY KEY,
                coin_id INTEGER NOT NULL,
                amount NUMERIC NOT NULL,
                date DATE NOT NULL,

                FOREIGN KEY (coin_id)
                    REFERENCES coins (id)
            )
        """
        curr.execute(sql_create)

        sql_create = """
            CREATE TABLE withdraws (
                id INTEGER PRIMARY KEY,
                coin_id INTEGER NOT NULL,
                amount NUMERIC NOT NULL,
                date DATE NOT NULL,

                FOREIGN KEY (coin_id)
                    REFERENCES coins (id)
            )
        """
        curr.execute(sql_create)

        sql_create = """
            CREATE TABLE tot_balances (
                date DATE NOT NULL PRIMARY KEY,
                eur_amount NUMERIC NOT NULL,
                usd_amount NUMERIC NOT NULL
            )
        """
        curr.execute(sql_create)

        conn.commit()
        conn.close()
        return True, "ok"

    except Exception as e:
        return False, f"{type(e).__name__} - {e}"
