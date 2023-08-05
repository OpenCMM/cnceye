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


def test_is_same_straight_line0():
    line0 = Line(Coordinate(-53.01875, 14.89375, -10), Coordinate(-53.01875, 28.0, -10))
    line1 = Line(
        Coordinate(-53.01875, 4.89375, -10), Coordinate(-53.01875, 25.125, -10)
    )
    assert line0.is_same_straight_line(line1)


def test_is_same_straight_line1():
    line0 = Line(Coordinate(-37.775, 20.66875, 10), Coordinate(37.775, 20.66875, 10))
    line1 = Line(Coordinate(-37.85625, 20.6625, 10), Coordinate(37.85625, 20.6625, 10))
    assert line0.is_same_straight_line(line1)


def test_is_overlapping0():
    line0 = Line(Coordinate(-53.01875, 14.89375, -10), Coordinate(-53.01875, 28.0, -10))
    line1 = Line(
        Coordinate(-53.01875, 4.89375, -10), Coordinate(-53.01875, 25.125, -10)
    )
    assert line0.is_overlapping(line1)

    line0 = Line(Coordinate(-53.01875, 14.89375, -10), Coordinate(-53.01875, 28.0, -10))
    line1 = Line(
        Coordinate(-53.01875, 4.89375, -10), Coordinate(-53.01875, 11.125, -10)
    )
    assert not line0.is_overlapping(line1)


def test_is_overlapping1():
    line0 = Line(
        Coordinate(-42.66875, 4.89375, -10), Coordinate(-42.66875, 15.76875, -10)
    )
    line1 = Line(Coordinate(-42.675, 4.89375, -10), Coordinate(-42.675, 15.675, -10))
    assert line0.is_overlapping(line1)
