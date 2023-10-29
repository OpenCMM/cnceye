from tests.config import MYSQL_CONFIG
from cnceye.edge import find
import mysql.connector
import sqlite3

process_id = 100


def copy_sqlite_db_to_mysql():
    db_path = "tests/fixtures/db/listener.db"
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


def test_find_edges():
    copy_sqlite_db_to_mysql()
    measured_edges = find.find_edges(process_id)
    assert len(measured_edges) > 32


def test_find_edge():
    filepath = "tests/fixtures/sensor/one_edge.csv"
    edge_position = find.find_edge(filepath)
    print(edge_position)


def test_find_edge_from_sqlite():
    db_path = "tests/fixtures/db/listener.db"
    measured_edges = find.find_edges_from_sqlite(db_path, 100.0)
    print(measured_edges)
    assert len(measured_edges) > 32


def test_add_measured_edge_coord():
    measured_edges = find.find_edges(process_id)
    edge_data = [
        (1, -50.0, -21.667, 10.0),
        (2, -50.0, 21.667, 10.0),
        (3, -25.0, 34.667, 10.0),
        (4, -25.0, 41.333, 10.0),
        (5, -16.667, -65.0, 10.0),
        (6, -16.667, 65.0, 10.0),
        (7, -6.667, 23.0, 10.0),
        (8, -6.667, 53.0, 10.0),
        (9, 6.667, 23.0, 10.0),
        (10, 6.667, 53.0, 10.0),
        (11, 16.667, -65.0, 10.0),
        (12, 16.667, 65.0, 10.0),
        (13, 25.0, 34.667, 10.0),
        (14, 25.0, 41.333, 10.0),
        (15, 50.0, -21.667, 10.0),
        (16, 50.0, 21.667, 10.0),
        (17, -25.0, 28.0, 10.0),
        (18, -24.289, 25.429, 10.0),
        (19, -22.357, 23.59, 10.0),
        (20, 20.0, 23.0, 10.0),
        (21, 22.571, 23.711, 10.0),
        (22, 24.41, 25.643, 10.0),
        (23, 25.0, 48.0, 10.0),
        (24, 24.289, 50.571, 10.0),
        (25, 22.357, 52.41, 10.0),
        (26, -20.0, 53.0, 10.0),
        (27, -22.571, 52.289, 10.0),
        (28, -24.41, 50.357, 10.0),
        (29, 9.0, -29.997, 10.0),
        (30, -4.5, -22.203, 10.0),
        (31, -4.5, -37.791, 10.0),
    ]
    # edge_data = find.get_edge_data(1)
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
