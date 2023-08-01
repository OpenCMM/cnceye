import cv2
from cnceye.cmm import Cmm
from cnceye.camera import Camera
from cnceye.coordinates import Coordinates
from cnceye.circle import get_circles
from cnceye.line import get_lines

focal_length = 50.0  # mm
camera_height = 60.0  # mm
object_height = 10.0  # mm
distance = camera_height - object_height
sensor_width = 36.0  # mm
camera = Camera(focal_length, sensor_width)


def diff_in_micron(expected, actual):
    return (expected - actual) * 1000


def test_opencv_coord_1():
    image = cv2.imread("tests/fixtures/output_images/image_1.png")
    center_coordinates = Coordinates((-50.0, 25.0, 60.0))

    cmm = Cmm(image, center_coordinates, camera)
    circles = get_circles(image, 100, 50, 100, 200)
    (x_pixel, y_pixel, r_pixel) = circles[0][0]

    # check radius is close to expected radius
    expected_radius = 3.0  # mm
    radius_from_img_in_mm = cmm.from_pixel_length(distance, r_pixel)
    radius_diff_in_micron = diff_in_micron(expected_radius, radius_from_img_in_mm)
    print(f"radius: {radius_diff_in_micron:.2f} μm")
    assert radius_diff_in_micron < 100.0

    # check center is close to expected center
    expected_circle_center = Coordinates((-48.0, 23.0, 10.0))
    circle_center_from_img_in_mm = cmm.from_opencv_coord(distance, (x_pixel, y_pixel))
    x_from_img_in_mm = circle_center_from_img_in_mm.x
    y_from_img_in_mm = circle_center_from_img_in_mm.y

    x_diff_in_micro = diff_in_micron(expected_circle_center.x, x_from_img_in_mm)
    print(f"x: {x_diff_in_micro:.2f} μm")
    assert x_diff_in_micro < 100.0

    y_diff_in_micron = diff_in_micron(expected_circle_center.y, y_from_img_in_mm)
    print(f"y: {y_diff_in_micron:.2f} μm")
    assert y_diff_in_micron < 100.0

    lines = get_lines(image)
    assert len(lines) > 0
    expected_corner = Coordinates((-53.0, 28.0, 10.0))
    x_pixel, y_pixel = lines[0][0][0], lines[0][0][1]
    corner_from_img_in_mm = cmm.from_opencv_coord(distance, (x_pixel, y_pixel))
    x_from_img_in_mm = corner_from_img_in_mm.x
    y_from_img_in_mm = corner_from_img_in_mm.y

    x_diff_in_micro = diff_in_micron(expected_corner.x, x_from_img_in_mm)
    print(f"x: {x_diff_in_micro:.2f} μm")
    assert x_diff_in_micro < 100.0

    y_diff_in_micron = diff_in_micron(expected_corner.y, y_from_img_in_mm)
    print(f"y: {y_diff_in_micron:.2f} μm")
    assert y_diff_in_micron < 100.0


def test_opencv_coord_2():
    image = cv2.imread("tests/fixtures/output_images/image_2.png")
    center_coordinates = Coordinates((-40.0, 25.0, 60.0))

    cmm = Cmm(image, center_coordinates, camera)
    circles = get_circles(image, 100, 50, 100, 200)
    (x_pixel, y_pixel, r_pixel) = circles[0][0]

    # check radius is close to expected radius
    expected_radius = 3.0  # mm
    radius_from_img_in_mm = cmm.from_pixel_length(distance, r_pixel)
    radius_diff_in_micron = diff_in_micron(expected_radius, radius_from_img_in_mm)
    print(f"radius: {radius_diff_in_micron:.2f} μm")
    assert radius_diff_in_micron < 100.0

    # check center is close to expected center
    expected_circle_center = Coordinates((-48.0, 23.0, 10.0))
    circle_center_from_img_in_mm = cmm.from_opencv_coord(distance, (x_pixel, y_pixel))
    x_from_img_in_mm = circle_center_from_img_in_mm.x
    y_from_img_in_mm = circle_center_from_img_in_mm.y

    x_diff_in_micro = diff_in_micron(expected_circle_center.x, x_from_img_in_mm)
    print(f"x: {x_diff_in_micro:.2f} μm")
    assert x_diff_in_micro < 100.0

    y_diff_in_micron = diff_in_micron(expected_circle_center.y, y_from_img_in_mm)
    print(f"y: {y_diff_in_micron:.2f} μm")
    assert y_diff_in_micron < 100.0

    lines = get_lines(image)
    assert len(lines) > 0
    expected_corner = Coordinates((-53.0, 28.0, 10.0))
    x_pixel, y_pixel = lines[0][0][0], lines[0][0][1]
    corner_from_img_in_mm = cmm.from_opencv_coord(distance, (x_pixel, y_pixel))
    x_from_img_in_mm = corner_from_img_in_mm.x
    y_from_img_in_mm = corner_from_img_in_mm.y

    x_diff_in_micro = diff_in_micron(expected_corner.x, x_from_img_in_mm)
    print(f"x: {x_diff_in_micro:.2f} μm")
    assert x_diff_in_micro < 100.0

    y_diff_in_micron = diff_in_micron(expected_corner.y, y_from_img_in_mm)
    print(f"y: {y_diff_in_micron:.2f} μm")
    assert y_diff_in_micron < 100.0


def test_opencv_coord_3():
    image = cv2.imread("tests/fixtures/output_images/image_3.png")
    center_coordinates = Coordinates((-30.0, 25.0, 60.0))

    cmm = Cmm(image, center_coordinates, camera)
    circles = get_circles(image, 100, 50, 100, 200)
    (x_pixel, y_pixel, r_pixel) = circles[0][0]

    # check radius is close to expected radius
    expected_radius = 3.0  # mm
    radius_from_img_in_mm = cmm.from_pixel_length(distance, r_pixel)
    radius_diff_in_micron = diff_in_micron(expected_radius, radius_from_img_in_mm)
    print(f"radius: {radius_diff_in_micron:.2f} μm")
    # assert radius_diff_in_micron < 100.0

    # check center is close to expected center
    expected_circle_center = Coordinates((-48.0, 23.0, 10.0))
    circle_center_from_img_in_mm = cmm.from_opencv_coord(distance, (x_pixel, y_pixel))
    x_from_img_in_mm = circle_center_from_img_in_mm.x
    y_from_img_in_mm = circle_center_from_img_in_mm.y

    x_diff_in_micro = diff_in_micron(expected_circle_center.x, x_from_img_in_mm)
    print(f"x: {x_diff_in_micro:.2f} μm")
    # assert x_diff_in_micro < 100.0

    y_diff_in_micron = diff_in_micron(expected_circle_center.y, y_from_img_in_mm)
    print(f"y: {y_diff_in_micron:.2f} μm")
    # assert y_diff_in_micron < 100.0

    lines = get_lines(image)
    assert len(lines) > 0
