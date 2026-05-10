import psycopg
from psycopg import sql


def select_all(cur: psycopg.Cursor, table: str):
    cur.execute(sql.SQL("SELECT * FROM sales.{}").format(sql.Identifier(table)))
    return cur.fetchall()


def select_join(cur: psycopg.Cursor, table: str, col1: str, col2: str):
    cur.execute(
        sql.SQL("SELECT {}, {} FROM sales.{}").format(
            sql.Identifier(col1), sql.Identifier(col2), sql.Identifier(table)
        )
    )
    return cur.fetchall()
