import csv


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


def find_line(filepath: str, edge_count: int, minimal_diff: float = 5.0):
    # read csv
    with open(filepath, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        data = list(reader)

    lines = []
    previous_distance = ""
    previous_row = None

    # x, y, z, distance
    for row in data:
        distance = row[3]
        if check_if_edge_is_found(distance, previous_distance, minimal_diff):
            if distance == "":
                lines.append(previous_row)
            else:
                lines.append(row)

            if len(lines) == edge_count:
                return lines
        previous_distance = distance
        previous_row = row
