import cv2
import numpy as np
from cnceye.coordinate import Coordinate


class Line:
    def __init__(self, start: Coordinate, end: Coordinate) -> None:
        self.start = start
        self.end = end

    def get_slope(self) -> float:
        return (self.end.y - self.start.y) / (self.end.x - self.start.x)

    def get_intercept(self) -> float:
        return self.start.y - self.get_slope() * self.start.x

    def get_x(self, y: float) -> float:
        return (y - self.get_intercept()) / self.get_slope()

    def get_y(self, x: float) -> float:
        return self.get_slope() * x + self.get_intercept()

    def get_length(self) -> float:
        return np.sqrt(
            (self.end.x - self.start.x) ** 2 + (self.end.y - self.start.y) ** 2
        )

    def get_intersection(self, other) -> tuple:
        x = (other.get_intercept() - self.get_intercept()) / (
            self.get_slope() - other.get_slope()
        )
        y = self.get_slope() * x + self.get_intercept()
        return (x, y)

    def __repr__(self) -> str:
        return f"Line({self.start}, {self.end})"


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
