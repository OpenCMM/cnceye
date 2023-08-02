import cv2
from cnceye.cmm import AllImages
from cnceye.camera import Camera
from cnceye.coordinate import Coordinate
from tests.utils import diff_in_micron

focal_length = 50.0  # mm
camera_height = 60.0  # mm
object_height = 10.0  # mm
distance = camera_height - object_height
sensor_width = 36.0  # mm
camera = Camera(focal_length, sensor_width)


def test_add_image():
    start = Coordinate(-50.0, 25.0, 60.0)
    move = Coordinate(10.0, 0.0, 0.0)
    all_images = AllImages(start, camera, move)
    for i in range(1, 11):
        image = cv2.imread(f"tests/fixtures/output_images/image_{i}.png")
        all_images.add_image(image, distance)

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
