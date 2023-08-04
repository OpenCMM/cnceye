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


def test_is_same_straight_line():
    line0 = Line(
        Coordinate(-53.01875, 14.89375, -100), Coordinate(-53.01875, 28.0, -100)
    )
    line1 = Line(
        Coordinate(-53.01875, 4.89375, -100), Coordinate(-53.01875, 25.125, -100)
    )
    assert line0.is_same_straight_line(line1)


def test_is_overlapping():
    line0 = Line(
        Coordinate(-53.01875, 14.89375, -100), Coordinate(-53.01875, 28.0, -100)
    )
    line1 = Line(
        Coordinate(-53.01875, 4.89375, -100), Coordinate(-53.01875, 25.125, -100)
    )
    assert line0.is_overlapping(line1)

    line0 = Line(
        Coordinate(-53.01875, 14.89375, -100), Coordinate(-53.01875, 28.0, -100)
    )
    line1 = Line(
        Coordinate(-53.01875, 4.89375, -100), Coordinate(-53.01875, 11.125, -100)
    )
    assert not line0.is_overlapping(line1)
