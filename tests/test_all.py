import cv2
from cnceye.cmm import AllImages
from cnceye.camera import Camera
from cnceye.coordinate import Coordinate
from tests.utils import diff_in_micron

import pytest

focal_length = 50.0  # mm
camera_height = 60.0  # mm
object_height = 10.0  # mm
distance = camera_height - object_height
sensor_width = 36.0  # mm
camera = Camera(focal_length, sensor_width)


@pytest.mark.skip(reason="need to fix")
def test_add_image_one_row():
    x_move = Coordinate(20.0, 0.0, 0.0)
    all_images = AllImages(camera)
    initial_center = Coordinate(-50.0, 25.0, 60.0)
    index = 0
    for i in range(0, 6):
        image = cv2.imread(f"tests/fixtures/output_images/image_{index}.png")
        center = initial_center + x_move * i
        all_images.add_image(image, distance, center)
        index += 1

    print(f"lines: {len(all_images.previous_lines)}")
    print(all_images.previous_lines)

    all_images.save_image("output/one_row.png")

    first_line = all_images.previous_lines[0]
    expected_first_line_length = 106.0
    first_line_diff_in_micron = diff_in_micron(
        expected_first_line_length, first_line.get_length()
    )
    print(f"first line length: {first_line_diff_in_micron:.2f} μm")
    assert first_line_diff_in_micron < 100.0

    third_line = all_images.previous_lines[2]
    expected_third_line_length = 75.0
    third_line_diff_in_micron = diff_in_micron(
        expected_third_line_length, third_line.get_length()
    )
    print(f"third line length: {third_line_diff_in_micron:.2f} μm")
    assert third_line_diff_in_micron < 100.0


@pytest.mark.skip(reason="need to fix")
def test_add_image_two_rows():
    x_move = Coordinate(20.0, 0.0, 0.0)
    y_move = Coordinate(0.0, -10.0, 0.0)
    all_images = AllImages(camera)
    index = 0
    initial_center = Coordinate(-50.0, 25.0, 60.0)
    for i in range(0, 2):
        for j in range(0, 6):
            image = cv2.imread(f"tests/fixtures/output_images/image_{index}.png")
            center = initial_center + x_move * j + y_move * i
            all_images.add_image(image, distance, center)
            index += 1

    line_count = len(all_images.previous_lines)
    print(f"line count: {line_count}")
    for line in all_images.previous_lines:
        print(line)

    all_images.save_image("output/two.png")

    first_line = all_images.previous_lines[0]
    expected_first_line_length = 106.0
    first_line_diff_in_micron = diff_in_micron(
        expected_first_line_length, first_line.get_length()
    )
    print(f"first line length: {first_line_diff_in_micron:.2f} μm")
    assert first_line_diff_in_micron < 100.0

    third_line = all_images.previous_lines[2]
    expected_third_line_length = 75.0
    third_line_diff_in_micron = diff_in_micron(
        expected_third_line_length, third_line.get_length()
    )
    print(f"third line length: {third_line_diff_in_micron:.2f} μm")
    assert third_line_diff_in_micron < 100.0


@pytest.mark.skip(reason="need to fix")
def test_add_image_all_rows():
    x_move = Coordinate(20.0, 0.0, 0.0)
    y_move = Coordinate(0.0, -10.0, 0.0)
    all_images = AllImages(camera)
    index = 0
    initial_center = Coordinate(-50.0, 25.0, 60.0)
    for i in range(0, 6):
        for j in range(0, 6):
            image = cv2.imread(f"tests/fixtures/output_images/image_{index}.png")
            center = initial_center + x_move * j + y_move * i
            all_images.add_image(image, distance, center)
            index += 1

    print(f"lines: {len(all_images.previous_lines)}")
    print(all_images.previous_lines)

    all_images.save_image("output/all.png")

    first_line = all_images.previous_lines[0]
    expected_first_line_length = 106.0
    first_line_diff_in_micron = diff_in_micron(
        expected_first_line_length, first_line.get_length()
    )
    print(f"first line length: {first_line_diff_in_micron:.2f} μm")
    assert first_line_diff_in_micron < 100.0

    third_line = all_images.previous_lines[2]
    expected_third_line_length = 75.0
    third_line_diff_in_micron = diff_in_micron(
        expected_third_line_length, third_line.get_length()
    )
    print(f"third line length: {third_line_diff_in_micron:.2f} μm")
    assert third_line_diff_in_micron < 100.0


def test_fetch_real_coordinates():
    all_images = AllImages(camera)
    all_images.fetch_real_coordinates()

def test_fetch_lines():
    all_images = AllImages(camera)
    all_images.fetch_lines()

def test_add_line():
    all_images = AllImages(camera)
    all_images.add_lines()
    all_images.save_image("output/lines.png")