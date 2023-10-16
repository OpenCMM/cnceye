import csv
import sqlite3
import mysql.connector
from mysql.connector.errors import IntegrityError

from cnceye.config import MYSQL_CONFIG


def find_edge(filepath: str, minimal_diff: float = 5.0):
    # read csv
    with open(filepath, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        data = list(reader)

    previous_distance = ""

    # x, y, z, distance
    for row in data:
        distance = row[3]
        if check_if_edge_is_found(distance, previous_distance, minimal_diff):
            return row
        previous_distance = distance


def find_edges_from_sqlite(database_path: str, minimal_diff: float = 5.0):
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    previous_distance = ""
    edges = []
    for row in cur.execute("SELECT * FROM coord"):
        # x, y, z, distance
        distance = row[4]
        if check_if_edge_is_found(distance, previous_distance, minimal_diff):
            edges.append(row)
        previous_distance = distance

    # remove the starting point
    edges.pop(0)
    return edges


def check_if_edge_is_found(
    distance: str, prev_distance: str or float, minimal_diff: float = 5.0
):
    if distance == "" and prev_distance == "":
        return False
    if distance == "" or prev_distance == "":
        return True
    if abs(float(distance) - float(prev_distance)) > minimal_diff:
        return True
    return False


def find_lines(filepath: str, edge_count: int, minimal_diff: float = 5.0):
    # read csv
    with open(filepath, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        data = list(reader)

    lines = []
    line = []
    previous_distance = ""
    previous_row = None

    # x, y, z, distance
    for row in data:
        distance = row[3]
        if check_if_edge_is_found(distance, previous_distance, minimal_diff):
            if distance == "":
                line.append(previous_row)
            else:
                line.append(row)

            if len(line) == edge_count:
                lines.append(line)
                line = []
        previous_distance = distance
        previous_row = row

    return lines


def get_edge_data():
    cnx = mysql.connector.connect(**MYSQL_CONFIG, database="coord")
    cursor = cnx.cursor()
    query = "SELECT id,side_id,x,y,z FROM edge"
    cursor.execute(query)
    edges = cursor.fetchall()
    cursor.close()
    cnx.close()
    return edges


def identify_close_edge(edges, measured_edges, distance_threshold=2.5):
    update_list = []
    for id, side_id, x, y, z in edges:
        min_distance = 999999.0
        data_with_min_distance = []
        for measured_edge in measured_edges:
            rx = measured_edge[1]
            ry = measured_edge[2]
            distance = ((x - rx) ** 2 + (y - ry) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                data_with_min_distance = (rx, ry, z, id)

        if min_distance <= distance_threshold:
            update_list.append(data_with_min_distance)

    return update_list


def add_measured_edge_coord(edge_list: list):
    cnx = mysql.connector.connect(**MYSQL_CONFIG, database="coord")
    cursor = cnx.cursor()
    insert_query = "UPDATE edge SET rx = %s, ry = %s, rz = %s WHERE id = %s"
    try:
        cursor.executemany(insert_query, edge_list)
    except IntegrityError:
        print("Error: unable to import lines")
    cnx.commit()
    cursor.close()
    cnx.close()