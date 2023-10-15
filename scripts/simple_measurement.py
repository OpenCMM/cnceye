import bpy
from mathutils import Vector
import sqlite3

# Get the active object (the 3D model)
obj = bpy.data.objects["test-part"]

# Define the ray's starting point in object space
x = 0.053
y = 0.0581
z = 0.206

start_point = Vector((x, y, z)) - obj.location
ray_direction = Vector((0, 0, -1))

# x, y, z, distance
data = []

slow = 0.05
fast = 0.6

# Ensure the object has a mesh
assert obj.type == "MESH"


def distance_to_analog_output(distance: float):
    distance = distance * 1000 * 135  # m to mm, distance to analog output
    return float(round(distance))


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
        distance = 0.14  # 140 mm
        # Calculate the intersection point with the face
        (hit, intersection_point, *_) = obj.ray_cast(_start_point, ray_direction)

        if hit:
            distance = _start_point[2] - intersection_point[2]

        # sensor_position in world space
        sensor_position = _start_point + obj.location
        # m to mm and round to 3 decimal places
        xyz = [sensor_position.x, sensor_position.y, sensor_position.z]
        xyz = [round(x * 1000, 3) for x in xyz]

        data.append([*xyz, distance_to_analog_output(distance)])
        _start_point = _start_point + Vector(tuple([x / 1000 for x in step]))

    return _start_point


start_point = move_start_point(start_point, (-fast, 0.0, 0.0), 110.0)
start_point = move_start_point(start_point, (0.0, -fast, 0.0), 68.5)

start_point = move_start_point(start_point, (fast, 0.0, 0.0), 110.0)
start_point = move_start_point(start_point, (0.0, -fast, 0.0), 40.0)
start_point = move_start_point(start_point, (-fast, 0.0, 0.0), 60.0)

start_point = move_start_point(start_point, (0.0, fast, 0.0), 140.0)

conn = sqlite3.connect("listener.db")
cur = conn.cursor()
cur.executemany("INSERT INTO coord(x, y, z, distance) VALUES (?, ?, ?, ?)", data)
conn.commit()
conn.close()

# result = [
#     (1, 53.0, 58.1, 206.0, 18900.0, "2023-10-12 12:12:57"),
#     (7, 49.4, 58.1, 206.0, 11925.0, "2023-10-12 12:12:57"),

#     (48, 24.8, 58.1, 206.0, 18900.0, "2023-10-12 12:12:57"),
#     (132, -25.6, 58.1, 206.0, 11925.0, "2023-10-12 12:12:57"),

#     (173, -50.2, 58.1, 206.0, 18900.0, "2023-10-12 12:12:57"),

#     (310, -49.6, -10.3, 206.0, 11925.0, "2023-10-12 12:12:57"),
#     (378, -8.8, -10.3, 206.0, 18900.0, "2023-10-12 12:12:57"),
#     (408, 9.2, -10.3, 206.0, 11925.0, "2023-10-12 12:12:57"),
#     (476, 50.0, -10.3, 206.0, 18900.0, "2023-10-12 12:12:57"),

#     (648, -1.6, -43.9, 206.0, 11925.0, "2023-10-12 12:12:57"),

#     (691, -1.6, -18.1, 206.0, 18900.0, "2023-10-12 12:12:57"),
#     (721, -1.6, -0.1, 206.0, 11925.0, "2023-10-12 12:12:57"),

#     (794, -1.6, 43.7, 206.0, 18900.0, "2023-10-12 12:12:57"),
#     (844, -1.6, 73.7, 206.0, 11925.0, "2023-10-12 12:12:57"),

#     (864, -1.6, 85.7, 206.0, 18900.0, "2023-10-12 12:12:57"),
# ]
