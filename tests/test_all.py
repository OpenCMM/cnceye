import cv2
from cnceye.cmm import AllImages
from cnceye.camera import Camera
from cnceye.coordinate import Coordinate

focal_length = 50.0  # mm
camera_height = 60.0  # mm
object_height = 10.0  # mm
distance = camera_height - object_height
sensor_width = 36.0  # mm
camera = Camera(focal_length, sensor_width)


def test_add():
    start = Coordinate(-50.0, 25.0, 60.0)
    move = Coordinate(10.0, 0.0, 0.0)
    all_images = AllImages(start, camera, move)
    for i in range(1, 11):
        image = cv2.imread(f"tests/fixtures/output_images/image_{i}.png")
        all_images.add_image(image, distance)

    print(f"lines: {len(all_images.previous_lines)}")
    print(all_images.previous_lines)

    all_images.save_image("output/all.png")