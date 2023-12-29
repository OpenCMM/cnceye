from cnceye import Shape
from cnceye.arc import (
    fit_circle,
    get_arc_info,
    get_edges_for_arc,
    is_circle,
)


def test_fit_circle():
    shape = Shape("tests/fixtures/stl/sample.stl")
    lines, arcs = shape.get_lines_and_arcs()
    for arc_points in arcs[0]:
        points = arc_points[:, :2]
        center_x, center_y, radius = fit_circle(points)
        assert radius > 0.0


def test_get_arc_info():
    shape = Shape("tests/fixtures/stl/sample.stl")
    lines, arcs = shape.get_lines_and_arcs()
    for arc_points in arcs[0]:
        radius, center = get_arc_info(arc_points)
        assert radius == 9.0 or radius == 5.0


def test_get_edges_for_arc():
    shape = Shape("tests/fixtures/stl/sample.stl")
    lines, arcs = shape.get_lines_and_arcs()
    for arc_points in arcs[0]:
        edges = get_edges_for_arc(arc_points, 3)
        assert len(edges) == 3


def test_get_edges_for_arc_many_edges():
    shape = Shape("tests/fixtures/stl/sample.stl")
    lines, arcs = shape.get_lines_and_arcs()
    for arc_points in arcs[0]:
        edges = get_edges_for_arc(arc_points, 4)
        assert len(edges) == 4

        edges = get_edges_for_arc(arc_points, 6)
        assert len(edges) == 6


def test_is_circle():
    shape = Shape("tests/fixtures/stl/sample.stl")
    lines, arcs = shape.get_lines_and_arcs()
    arcs = arcs[0]
    assert not is_circle(arcs[0])
    assert not is_circle(arcs[1])
    assert not is_circle(arcs[2])
    assert not is_circle(arcs[3])
    assert is_circle(arcs[4])
