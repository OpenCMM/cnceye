import cv2
import numpy as np


def get_lines(
    image,
    gaussian_blur_size=5,
    canny_low_threshold=100,
    canny_high_threshold=200,
    rho=0.1,
    hough_threshold=50,
    min_line_length=50,
    max_line_gap=200,
):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_gray = cv2.GaussianBlur(gray, (gaussian_blur_size, gaussian_blur_size), 0)
    edges = cv2.Canny(
        blur_gray,
        canny_low_threshold,
        canny_high_threshold,
        apertureSize=3,
        L2gradient=True,
    )
    edges = cv2.dilate(edges, None, iterations=1)
    edges = cv2.erode(edges, None, iterations=1)

    lines = cv2.HoughLinesP(
        edges,
        rho,
        np.pi / 180 * rho,
        hough_threshold,
        minLineLength=min_line_length,
        maxLineGap=max_line_gap,
    )
    return lines
