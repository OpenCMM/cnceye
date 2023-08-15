import cv2
from cnceye.cmm import SingleImage
from cnceye.camera import Camera
from cnceye.coordinate import Coordinate
from tests.utils import diff_in_micron

focal_length = 50.0  # mm
camera_height = 10.5  # mm
object_height = 10.0  # mm
distance = camera_height - object_height
sensor_width = 36.0  # mm
camera = Camera(focal_length, sensor_width)


def test_image_0():
    image = cv2.imread("tests/fixtures/images/image_0.png")
    center_coordinates = Coordinate(-50.0, 65.0, object_height)

    cmm = SingleImage(image, center_coordinates, camera)
    vertex = cmm.vertex(distance)
    x_diff_in_micro = diff_in_micron(-50.0, vertex.x)
    print(f"x: {x_diff_in_micro:.2f} μm")
    assert x_diff_in_micro < 1.0
    y_diff_in_micron = diff_in_micron(65.0, vertex.y)
    print(f"y: {y_diff_in_micron:.2f} μm")
    assert y_diff_in_micron < 1.0
    cmm.add_real_coordinate(distance)


def test_add_real_coordinate():
    index = 0
    with open("scripts/coordinates.txt") as f:
        for line in f:
            xyz = line.strip().split(",")
            x, y, z = [float(i) for i in xyz]

            image = cv2.imread(f"tests/fixtures/images/image_{index}.png")
            center_coordinates = Coordinate(x, y, z)
            cmm = SingleImage(image, center_coordinates, camera)
            cmm.add_real_coordinate(distance)
            index += 1


def test_add_real_coordinate_with_real_images():
    index = 0
    with open("scripts/test.txt") as f:
        for line in f:
            xyz = line.strip().split(",")
            x, y, z = [float(i) for i in xyz]

            image = cv2.imread(f"tests/fixtures/images/test{index}.jpg")
            center_coordinates = Coordinate(x, y, z)
            cmm = SingleImage(image, center_coordinates, camera)
            cmm.add_real_coordinate(distance)
            index += 1
