from cnceye.coordinate import Coordinate
from cnceye.camera import Camera
from .pixel import get_field_of_view, get_pixel_per_mm
import numpy as np
from cnceye.line import get_lines, Line
from typing import List


class Cmm:
    def __init__(self, image, center_coordinate: Coordinate, camera: Camera) -> None:
        self.image = image
        self.center = center_coordinate
        self.camera = camera

    def get_opencv_origin(self, image, distance: float) -> Coordinate:
        # opencv origin is at top left corner
        pixel_per_mm = self.pixel_per_mm(distance)
        diff_in_pixel = (-image.shape[1] / 2, image.shape[0] / 2, 0)
        diff_in_mm = np.array([x / pixel_per_mm for x in diff_in_pixel])
        return self.center + diff_in_mm

    def pixel_per_mm(self, distance: float) -> float:
        field_of_view = get_field_of_view(
            self.camera.focal_length, self.camera.sensor_width, distance
        )
        return get_pixel_per_mm(field_of_view, self.image.shape[1])

    def from_opencv_coord(self, distance: float, opencv_xy: tuple) -> Coordinate:
        pixel_per_mm = self.pixel_per_mm(distance)
        opencv_origin = self.get_opencv_origin(self.image, distance)

        return Coordinate(
            opencv_origin.x + opencv_xy[0] / pixel_per_mm,
            opencv_origin.y - opencv_xy[1] / pixel_per_mm,
            self.center.x - distance,
        )

    def from_pixel_length(self, distance: float, pixel_length) -> float:
        pixel_per_mm = self.pixel_per_mm(distance)
        return pixel_length / pixel_per_mm

    def lines(self, distance: float) -> List[Line] or None:
        line_array = get_lines(self.image)
        if line_array is None:
            return None

        lines = []
        for line in line_array:
            x1, y1, x2, y2 = line[0]
            start = self.from_opencv_coord(distance, (x1, y1))
            end = self.from_opencv_coord(distance, (x2, y2))
            lines.append(Line(start, end))

        return lines
