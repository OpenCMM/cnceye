"""
Simulate the measurement of the 3D model by moving the sensor with G-code
"""
import bpy
from mathutils import Vector
import csv
import sys

# Get the active object (the 3D model)
obj = bpy.data.objects["test-part"]

ray_direction = Vector((0, 0, -1))

# x, y, z, distance
data = []

# Ensure the object has a mesh
assert obj.type == "MESH"


def distance_to_analog_output(distance: float):
    distance = distance * 1000 * 135  # m to mm, distance to analog output
    return float(round(distance))


def load_gcode(filepath: str):
    with open(filepath, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=" ")
        gcode = list(reader)
    gcode = gcode[2:-2]
    return gcode


def move_start_point(_start_point, xyz, feedrate: float):
    """
    Move the start point to the given direction
    _start_point: Vector (x, y, z) in m (relative to obj.location)
    xyz: tuple (x, y, z) in mm
    feedrate: float (mm/min)
    sensor response time is 10ms
    """
    one_step_distance = feedrate / 1000 / 60 * 0.01  # m/step
    destination = Vector(tuple([x / 1000 for x in xyz]))
    total_distance_to_move = (destination - _start_point).length
    loop_count = int(total_distance_to_move // one_step_distance)
    move_vector = (destination - _start_point) / loop_count
    for _ in range(loop_count):
        distance = 0.14  # 140 mm
        # Calculate the intersection point with the face
        (hit, intersection_point, *_) = obj.ray_cast(_start_point, ray_direction)

        if hit:
            distance = start_point[2] - intersection_point[2]

        # m to mm and round to 3 decimal places
        xyz = [_start_point.x, _start_point.y, _start_point.z]
        xyz = [round(x * 1000, 3) for x in xyz]

        data.append([*xyz, distance_to_analog_output(distance)])
        _start_point = _start_point + move_vector

    return destination  # _start_point not may not become exactly the destination


def row_to_xyz_feedrate(row):
    x = float(row[1][1:])
    y = float(row[2][1:])
    z = float(row[3][1:])
    feedrate = float(row[4][1:])
    return (x, y, z, feedrate)


# get filepath from arguments
argv = sys.argv
argv = argv[argv.index("--") + 1 :]
assert len(argv) == 1
gcode = load_gcode(argv[0])

# Define the ray's starting point in object space
first_row = gcode[0]
(x, y, z, feedrate) = row_to_xyz_feedrate(first_row)
start_point = Vector((x / 1000, y / 1000, 0.206))


# start_point = Vector(initial_coord) - obj.location
gcode = gcode[1:]

for row in gcode:
    (x, y, z, feedrate) = row_to_xyz_feedrate(row)
    z = 206.0  # ignore z
    start_point = move_start_point(start_point, (x, y, z), feedrate)

# save as csv

output_folder = "/home/runner/work/cnceye/cnceye/output"
with open(f"{output_folder}/demo.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerows(data)
