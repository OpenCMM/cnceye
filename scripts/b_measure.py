"""
Simulate the measurement of the 3D model by moving the sensor with G-code
"""
import bpy
from mathutils import Vector
import sqlite3
import csv
import sys
import random

test_file = "<test-file>"

# import stl file
bpy.ops.import_mesh.stl(filepath=f"{test_file}.STL")

# Get the active object (the 3D model)
obj = bpy.data.objects[test_file]

ray_direction = Vector((0, 0, -1))

# x, y, z, distance
data = []
current_data = 100000
threshold = 100

# Ensure the object has a mesh
assert obj.type == "MESH"


def distance_to_analog_output(distance: float):
    distance = distance * 135  # distance to analog output
    # add noise
    distance = distance + (distance * 0.001 * (2 * random.random() - 1))
    return round(distance)


def load_gcode(filepath: str):
    with open(filepath, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=" ")
        gcode = list(reader)
    gcode = gcode[3:-2]
    return gcode


def move_start_point(_start_point, xyz, feedrate: float):
    """
    Move the start point to the given direction
    _start_point: Vector (x, y, z) (relative to obj.location)
    xyz: tuple (x, y, z) in mm
    feedrate: float (mm/min)
    sensor response time is 10ms
    """
    global current_data
    one_step_distance = feedrate / 60 * 0.01  # m/step
    destination = Vector(tuple([x for x in xyz]))
    total_distance_to_move = (destination - _start_point).length
    loop_count = int(total_distance_to_move // one_step_distance)
    move_vector = (destination - _start_point) / loop_count
    for _ in range(loop_count):
        distance = 140  # 140 mm
        # Calculate the intersection point with the face
        (hit, intersection_point, *_) = obj.ray_cast(_start_point, ray_direction)

        if hit:
            distance = start_point[2] - intersection_point[2]

        # m to mm and round to 3 decimal places
        xyz = [_start_point.x, _start_point.y, _start_point.z]
        xyz = [round(x, 3) for x in xyz]

        _sensor_data = distance_to_analog_output(distance)
        if abs(_sensor_data - current_data) > threshold:
            data.append([*xyz, _sensor_data])
            print(_sensor_data, current_data)
            current_data = _sensor_data
        _start_point = _start_point + move_vector

    return destination  # _start_point not may not become exactly the destination


def row_to_xyz_feedrate(row):
    x = float(row[1][1:])
    y = float(row[2][1:])
    feedrate = float(row[3][1:])
    return (x, y, feedrate)


# get filepath from arguments
argv = sys.argv
argv = argv[argv.index("--") + 1 :]
assert len(argv) == 1
gcode = load_gcode(argv[0])

# Define the ray's starting point in object space
first_row = gcode[0]
(x, y, feedrate) = row_to_xyz_feedrate(first_row)
start_point = Vector((x, y, 106))


# start_point = Vector(initial_coord) - obj.location
gcode = gcode[1:]

for row in gcode:
    (x, y, feedrate) = row_to_xyz_feedrate(row)
    print(x, y, feedrate)
    z = 106.0  # ignore z
    start_point = move_start_point(start_point, (x, y, z), feedrate)

conn = sqlite3.connect("listener.db")
cur = conn.cursor()
cur.executemany("INSERT INTO coord(x, y, z, distance) VALUES (?, ?, ?, ?)", data)
conn.commit()
conn.close()
