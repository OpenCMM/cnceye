import cv2
import numpy as np
from cnceye.coordinate import Coordinate


class Line:
    def __init__(self, start: Coordinate, end: Coordinate) -> None:
        # start.x < end.x
        if start.x > end.x:
            self.start = end
            self.end = start
        else:
            self.start = start
            self.end = end

    def get_slope(self) -> float:
        if self.end.x == self.start.x:
            return np.inf
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

    def is_same_straight_line(self, other: "Line") -> bool:
        return (
            self.get_slope() == other.get_slope()
            and self.get_intercept() == other.get_intercept()
        )
    
    def is_overlapping(self, other: "Line") -> bool:
        return (
            self.end.x >= other.start.x
            or self.start.x <= other.end.x
        )

    def connect_lines(self, other: "Line") -> "Line" or None:
        if self.is_same_straight_line(other) and self.is_overlapping(other):
            return Line(
                Coordinate(
                    min(self.start.x, other.start.x),
                    min(self.start.y, other.start.y),
                    self.start.z,
                ),
                Coordinate(
                    max(self.end.x, other.end.x),
                    max(self.end.y, other.end.y),
                    self.start.z,
                ),
            )

    def __repr__(self) -> str:
        return f"Line({self.start}, {self.end})"


def get_lines(
    image,
    gaussian_blur_size=5,
    canny_low_threshold=100,
    canny_high_threshold=200,
    rho=0.1,
    hough_threshold=100,
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
