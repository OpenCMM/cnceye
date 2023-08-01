from typing import Tuple


class Coordinates(Tuple):
    def __init__(self, xyz: Tuple[float]) -> None:
        super().__init__()
        self.x = xyz[0]
        self.y = xyz[1]
        self.z = xyz[2]
