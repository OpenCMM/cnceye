import cv2
from cnceye.camera import calib


def test_undistort_img():
    image = cv2.imread("tests/fixtures/images/coins.jpg")
    camera_data_path = "tests/fixtures/camera/google-pixel5-5g.json"
    _undistorted_image = calib.undistort_img(image, camera_data_path)
