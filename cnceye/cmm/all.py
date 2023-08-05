from cnceye.coordinate import Coordinate
from cnceye.camera import Camera
from cnceye.cmm.single import SingleImage
import cv2
import numpy as np


class AllImages:
    def __init__(self, camera: Camera) -> None:
        self.camera = camera
        self.previous_lines = []

    def add_image(self, image, distance: float, center: Coordinate) -> None:
        single = SingleImage(image, center, self.camera)
        lines = single.lines(distance)
        if lines is None:
            return None

        if len(self.previous_lines) == 0:
            self.previous_lines = lines
            return None

        for line in lines:
            is_new_line = True
            for i, previous_line in enumerate(self.previous_lines):
                new_line = line.connect_lines(previous_line)
                if new_line is not None:
                    self.previous_lines[i] = new_line
                    is_new_line = False
                    break

            if is_new_line:
                self.previous_lines.append(line)

    def save_image(self, path: str) -> None:
        entire_image = np.asarray([[[0, 0, 0]] * 1200] * 1000, dtype=np.uint8)
        for line in self.previous_lines:
            start = line.start
            end = line.end
            cv2.line(
                entire_image,
                (int((start.x + 100) * 5), int((-start.y + 100) * 5)),
                (int((end.x + 100) * 5), int((-end.y + 100) * 5)),
                (255, 255, 255),
                1,
            )
            cv2.putText(
                entire_image,
                f"{line.get_length():.2f}",
                (
                    int((start.x + end.x + 200) * 5 / 2),
                    int((-start.y - end.y + 200) * 5 / 2),
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (105, 145, 209),
                1,
            )
        cv2.imwrite(path, entire_image)
