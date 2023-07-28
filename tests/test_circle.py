from cnceye import circle
from cnceye import camera
import cv2


def test_get_circle():
    image = cv2.imread("tests/fixtures/images/coins.jpg")
    undistorted_image = camera.undistort_img(
        image, "tests/fixtures/camera/google-pixel5-5g.json"
    )

    circles = circle.get_circles(undistorted_image)
    assert len(circles) > 0
