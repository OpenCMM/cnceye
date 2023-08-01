from cnceye import circle
from cnceye.camera import calib
import cv2


def test_get_circle():
    image = cv2.imread("tests/fixtures/images/coins.jpg")
    undistorted_image = calib.undistort_img(
        image, "tests/fixtures/camera/google-pixel5-5g.json"
    )

    circles = circle.get_circles(undistorted_image, 100, 200, 100, 200)
    assert len(circles) > 0
