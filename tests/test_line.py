from cnceye.line import Line
from cnceye.coordinate import Coordinate
import numpy as np


def test_get_slope():
    start = Coordinate(0, 0, 0)
    end = Coordinate(1, 1, 0)
    line = Line(start, end)
    assert line.get_slope() == 1.0


def test_get_intercept():
    start = Coordinate(0, 0, 0)
    end = Coordinate(1, 1, 0)
    line = Line(start, end)
    assert line.get_intercept() == 0.0


def test_get_x():
    start = Coordinate(0, 0, 0)
    end = Coordinate(1, 1, 0)
    line = Line(start, end)
    assert line.get_x(1) == 1.0


def test_get_y():
    start = Coordinate(0, 0, 0)
    end = Coordinate(1, 1, 0)
    line = Line(start, end)
    assert line.get_y(1) == 1.0


def test_get_length():
    start = Coordinate(0, 0, 0)
    end = Coordinate(1, 1, 0)
    line = Line(start, end)
    assert line.get_length() == np.sqrt(2)


def test_get_intersection():
    start = Coordinate(0, 0, 0)
    end = Coordinate(1, 1, 0)
    line = Line(start, end)

    start = Coordinate(0, 1, 0)
    end = Coordinate(1, 0, 0)
    other = Line(start, end)
    assert line.get_intersection(other) == (0.5, 0.5)
