from cnceye.config import MYSQL_CONFIG
from cnceye.edge import find
import mysql.connector
import sqlite3


def copy_sqlite_db_to_mysql():
    db_path = "tests/fixtures/db/listener.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "SELECT x,y,z,distance FROM coord"
    data = []
    for row in cur.execute(query):
        data.append(row)
    cur.close()
    conn.close()

    mysql_conn = mysql.connector.connect(**MYSQL_CONFIG, database="coord")
    mysql_cur = mysql_conn.cursor()
    mysql_cur.executemany(
        "INSERT INTO sensor(x, y, z, distance) VALUES (%s, %s, %s, %s)", data
    )
    mysql_conn.commit()
    mysql_cur.close()
    mysql_conn.close()


def test_find_edges():
    copy_sqlite_db_to_mysql()
    measured_edges = find.find_edges()
    assert len(measured_edges) == 16


def test_find_edge():
    filepath = "tests/fixtures/sensor/one_edge.csv"
    edge_position = find.find_edge(filepath)
    print(edge_position)


def test_find_edge_from_sqlite():
    db_path = "tests/fixtures/db/listener.db"
    measured_edges = find.find_edges_from_sqlite(db_path, 100.0)
    print(measured_edges)
    assert len(measured_edges) == 16


def test_add_measured_edge_coord():
    measured_edges = find.find_edges()
    edge_data = [
        (1, 6, -50.0, 0.0, 10.0),
        (2, 8, -25.0, 38.0, 10.0),
        (3, 2, 0.0, -65.0, 10.0),
        (4, 3, 0.0, 23.0, 10.0),
        (5, 4, 0.0, 53.0, 10.0),
        (6, 1, 0.0, 65.0, 10.0),
        (7, 7, 25.0, 38.0, 10.0),
        (8, 5, 50.0, 0.0, 10.0),
    ]
    # edge_data = find.get_edge_data()
    update_list = find.identify_close_edge(edge_data, measured_edges)
    find.add_measured_edge_coord(update_list)


def test_check_if_edge_is_found():
    assert find.check_if_edge_is_found("", "") is False
    assert find.check_if_edge_is_found("", 100.0) is True
    assert find.check_if_edge_is_found(100.0, "") is True
    assert find.check_if_edge_is_found(100.0, 99.9) is False
    assert find.check_if_edge_is_found(100.0, 50.0) is True
    assert find.check_if_edge_is_found(50.0, 100.0) is True
    assert find.check_if_edge_is_found(99.9, 100.0) is False
    assert find.check_if_edge_is_found(99.0, 100.0, 0.1) is True


def test_find_line():
    filepath = "tests/fixtures/sensor/line.csv"
    lines = find.find_lines(filepath, 3)
    assert len(lines) == 1
    line = lines[0]
    expected_x = 50.0
    for row in line:
        x = float(row[0])
        assert x == expected_x


def test_find_lines():
    filepath = "tests/fixtures/sensor/lines.csv"
    lines = find.find_lines(filepath, 3)
    assert len(lines) == 4
    for line in lines:
        print(line)
