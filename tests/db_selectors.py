from typing import TypeVar

import psycopg
from psycopg import sql

_Row = TypeVar("_Row")


def select_all(cur: psycopg.Cursor[_Row], table: str) -> list[_Row]:
    cur.execute(sql.SQL("SELECT * FROM sales.{}").format(sql.Identifier(table)))
    return cur.fetchall()


def select_join(
    cur: psycopg.Cursor[_Row], table: str, col1: str, col2: str
) -> list[_Row]:
    cur.execute(
        sql.SQL("SELECT {}, {} FROM sales.{}").format(
            sql.Identifier(col1), sql.Identifier(col2), sql.Identifier(table)
        )
    )
    return cur.fetchall()
