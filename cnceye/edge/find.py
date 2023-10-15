import csv
import sqlite3


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
