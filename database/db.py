import pyodbc
from config import Config


def get_connection():
    conn_str = (
            f"DRIVER={{{Config.DB_DRIVER}}};"
            f"SERVER={Config.DB_SERVER};"
            f"DATABASE={Config.DB_NAME};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
    return pyodbc.connect(conn_str)


def fetch_all(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return rows


def fetch_one(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return dict(zip(columns, row)) if row else None


def execute(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    rowcount = cursor.rowcount
    cursor.close()
    conn.close()
    return rowcount


# def execute_return_id(query, params=()):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute(query, params)
#     cursor.execute("SELECT @@IDENTITY AS id")
#     new_id = cursor.fetchone()[0]
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return int(new_id)

def execute_return_id(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query + "; SELECT SCOPE_IDENTITY() AS id;", params)
    cursor.nextset()
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return int(row[0]) if row else None