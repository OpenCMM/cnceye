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


def move_x_axis(_start_point, step: float):
    for i in range(200):
        distance = None
        # Calculate the intersection point with the face
        (hit, intersection_point, *_) = obj.ray_cast(_start_point, ray_direction)

        if hit:
            distance = _start_point[2] - intersection_point[2]
            # distance = (start_point - intersection_point).length

            # intersection_point in world space
            # intersection_point = intersection_point + obj.location

        # sensor_position in world space
        sensor_position = _start_point + obj.location
        # m to mm and round to 3 decimal places
        xyz = [sensor_position.x, sensor_position.y, sensor_position.z]
        xyz = [round(x * 1000, 3) for x in xyz]

        data.append([*xyz, distance])
        _start_point = _start_point + Vector((step, 0, 0.0))

    return _start_point


def move_y_axis(_start_point, step: float):
    for i in range(100):
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
        _start_point = _start_point + Vector((0, step, 0.0))

    return _start_point


start_point = move_x_axis(start_point, -0.00005)
start_point = move_y_axis(start_point, -0.0006)
start_point = move_x_axis(start_point, 0.00005)
start_point = move_y_axis(start_point, -0.0006)
start_point = move_x_axis(start_point, -0.00005)

# save as csv
with open("line.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerows(data)
