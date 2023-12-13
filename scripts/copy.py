from tests.config import MYSQL_CONFIG
import mysql.connector
import sqlite3

process_id = 1


def copy_sqlite_db_to_mysql():
    db_path = "listener.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "SELECT x,y,z,distance FROM coord"
    data = []
    for row in cur.execute(query):
        row = (*row, process_id)
        data.append(row)
    cur.close()
    conn.close()

    mysql_conn = mysql.connector.connect(**MYSQL_CONFIG, database="coord")
    mysql_cur = mysql_conn.cursor()
    mysql_cur.executemany(
        "INSERT INTO sensor(x, y, z, distance, process_id) VALUES (%s,%s,%s, %s, %s)",
        data,
    )
    mysql_conn.commit()
    mysql_cur.close()
    mysql_conn.close()


copy_sqlite_db_to_mysql()
