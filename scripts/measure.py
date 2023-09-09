import bpy
from mathutils import Vector
import csv

# Get the active object (the 3D model)
obj = bpy.data.objects["test-part"]

# Define the ray's starting point in object space
x = 0.0567
y = 0.0316
z = 0.206

start_point = Vector((x, y, z)) - obj.location
ray_direction = Vector((0, 0, -1))

# x, y, z, distance
data = []

# Ensure the object has a mesh
assert obj.type == "MESH"

for i in range(200):
    distance = None
    # Calculate the intersection point with the face
    (hit, intersection_point, *_) = obj.ray_cast(start_point, ray_direction)

    if hit:
        distance = start_point[2] - intersection_point[2]
        # distance = (start_point - intersection_point).length

        # intersection_point in world space
        # intersection_point = intersection_point + obj.location

    # sensor_position in world space
    sensor_position = start_point + obj.location
    # m to mm and round to 3 decimal places
    xyz = [sensor_position.x, sensor_position.y, sensor_position.z]
    xyz = [round(x * 1000, 3) for x in xyz]

    data.append([*xyz, distance])
    # move start_point by 50μm
    start_point = start_point + Vector((-0.00005, 0, 0.0))

# save as csv
with open("output.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerows(data)
