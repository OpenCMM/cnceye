import bpy
from mathutils import Vector
import csv

# Get the active object (the 3D model)
obj = bpy.data.objects["test-part"]

# Define the ray's starting point in object space
x = 0.0567
y = 0.0846
z = 0.206

start_point = Vector((x, y, z)) - obj.location
ray_direction = Vector((0, 0, -1))

# x, y, z, distance
data = []

# Ensure the object has a mesh
assert obj.type == "MESH"


def move_start_point(_start_point, step, total_distance_to_move: float):
    """
    Move the start point to the given direction
    _start_point: Vector
    step: tuple (x, y, z) in mm
    total_distance_to_move: float in mm
    return Vector
    """
    one_step_distance = Vector(step).length
    loop_count = int(total_distance_to_move // one_step_distance)
    for _ in range(loop_count):
        distance = None
        # Calculate the intersection point with the face
        (hit, intersection_point, *_) = obj.ray_cast(_start_point, ray_direction)

        if hit:
            distance = _start_point[2] - intersection_point[2]

        # sensor_position in world space
        sensor_position = _start_point + obj.location
        # m to mm and round to 3 decimal places
        xyz = [sensor_position.x, sensor_position.y, sensor_position.z]
        xyz = [round(x * 1000, 3) for x in xyz]

        data.append([*xyz, distance])
        _start_point = _start_point + Vector(tuple([x / 1000 for x in step]))

    return _start_point


# left-top corner to right-bottom corner
start_point = move_start_point(start_point, (-0.05, 0.0, 0.0), 10.0)
start_point = move_start_point(start_point, (0.0, -0.6, 0.0), 62.0)
start_point = move_start_point(start_point, (0.05, 0.0, 0.0), 10.0)
start_point = move_start_point(start_point, (0.0, -0.6, 0.0), 62.0)
start_point = move_start_point(start_point, (-0.05, 0.0, 0.0), 10.0)

# right-bottom corner to left-bottom corner
start_point = move_start_point(start_point, (0.0, -0.05, 0.0), 10.0)
start_point = move_start_point(start_point, (-0.6, 0.0, 0.0), 48.5)
start_point = move_start_point(start_point, (0.0, 0.05, 0.0), 10.0)
start_point = move_start_point(start_point, (-0.6, 0.0, 0.0), 48.5)
start_point = move_start_point(start_point, (0.0, -0.05, 0.0), 10.0)

# left-bottom corner to left-top corner
start_point = move_start_point(start_point, (-0.5, 0.0, 0.0), 10.0)
start_point = move_start_point(start_point, (0.0, 0.5, 0.0), 10.0)
start_point = move_start_point(start_point, (0.05, 0.0, 0.0), 10.0)
start_point = move_start_point(start_point, (0.0, 0.6, 0.0), 62.0)
start_point = move_start_point(start_point, (-0.05, 0.0, 0.0), 10.0)
start_point = move_start_point(start_point, (0.0, 0.6, 0.0), 62.0)
start_point = move_start_point(start_point, (0.05, 0.0, 0.0), 10.0)

# left-top corner to right-top corner
start_point = move_start_point(start_point, (0.0, 0.05, 0.0), 10.0)
start_point = move_start_point(start_point, (0.6, 0.0, 0.0), 48.5)
start_point = move_start_point(start_point, (0.0, -0.05, 0.0), 10.0)
start_point = move_start_point(start_point, (0.6, 0.0, 0.0), 48.5)
start_point = move_start_point(start_point, (0.0, 0.05, 0.0), 10.0)

# save as csv
with open("lines.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerows(data)
