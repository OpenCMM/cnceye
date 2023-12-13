import random
import csv


def distance_to_analog_output(distance: float):
    """
    distance: float in m
    """
    distance = distance * 1000 * 135  # m to mm, distance to analog output
    # add noise
    distance = distance + (distance * 0.001 * (2 * random.random() - 1))
    return round(distance)


def test_distance_to_analog_output():
    distance_in_mm = 10.5
    analog_output = distance_to_analog_output(distance_in_mm / 1000)
    assert analog_output > 0
    assert analog_output < 19000


def load_gcode(filepath: str):
    with open(filepath, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=" ")
        gcode = list(reader)
    gcode = gcode[3:-2]
    return gcode


def row_to_xyz_feedrate(row):
    x = float(row[1][1:])
    y = float(row[2][1:])
    feedrate = float(row[3][1:])
    return (x, y, feedrate)


def test_load_gcode():
    gcode = load_gcode("tests/fixtures/gcode/edge.gcode")
    for row in gcode:
        (x, y, feedrate) = row_to_xyz_feedrate(row)
