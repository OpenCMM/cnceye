from cnceye import Shape
import pytest
import cadquery as cq


def test_are_facets_on_same_plane():
    shape = Shape("tests/fixtures/stl/step.STL")
    assert shape.are_coplanar(7, 8) is True
    assert shape.are_coplanar(7, 11) is False
    assert shape.are_coplanar(11, 12) is True


def test_grounp_by_coplanar_facets():
    shape = Shape("tests/fixtures/stl/sample.stl")
    visible_facet_indices = shape.get_visible_facets()
    group_facets = shape.group_by_coplanar_facets(visible_facet_indices)
    assert len(group_facets) == 1


def test_grounp_by_coplanar_facets_with_step_slope():
    shape = Shape("tests/fixtures/stl/step.STL")
    visible_facet_indices = shape.get_visible_facets()
    group_facets = shape.group_by_coplanar_facets(visible_facet_indices)
    assert len(group_facets) == 3


def test_group_by_coplanar_facets():
    shape = Shape("tests/fixtures/stl/sample.stl")
    visible_facets = shape.get_visible_facets()
    facet_groups = shape.group_by_coplanar_facets(visible_facets)
    assert len(facet_groups) == 1


def test_group_by_coplanar_facets_with_step_slope():
    shape = Shape("tests/fixtures/stl/step.STL")
    visible_facets = shape.get_visible_facets()
    facet_groups = shape.group_by_coplanar_facets(visible_facets)
    assert len(facet_groups) == 3
    assert len(facet_groups[0]) == 2
    assert len(facet_groups[1]) == 2
    assert len(facet_groups[2]) == 2


def test_lines_and_arcs():
    shape = Shape("tests/fixtures/stl/sample.stl")
    lines, arcs = shape.get_lines_and_arcs()

    assert len(lines) == 1
    assert len(arcs) == 1

    assert len(lines[0]) == 8
    assert len(arcs[0]) == 5


def test_get_lines_and_arcs_with_step_slope():
    shape = Shape("tests/fixtures/stl/step.STL")
    lines, arcs = shape.get_lines_and_arcs()

    assert len(lines) == 3
    assert len(arcs) == 0

    assert len(lines[0]) == 4
    assert len(lines[1]) == 4
    assert len(lines[2]) == 4


def test_get_arc_info():
    shape = Shape("tests/fixtures/stl/sample.stl")
    lines, arcs = shape.get_lines_and_arcs()
    for arc_points in arcs[0]:
        radius, center, is_circle = shape.get_arc_info(arc_points)
        assert radius == 9.0 or radius == 5.0

def test_cadquery_models():
    height = 60.0
    width = 80.0
    thickness = 10.0
    diameter = 22.0
    result = (
        cq.Workplane("XY")
        .box(height, width, thickness)
        .faces(">Z")
        .workplane()
        .hole(diameter)
    )
    stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
    cq.exporters.export(result, stl_filename)
    shape = Shape(stl_filename)
    lines, arcs = shape.get_lines_and_arcs()

    assert len(lines) == 1
    assert len(arcs) == 1

    assert len(lines[0]) == 4
    assert len(arcs[0]) == 1

def test_cadquery_models_more_holes():
    height = 60.0
    width = 80.0
    thickness = 10.0
    diameter = 22.0
    padding = 12.0

    result = (
        cq.Workplane("XY")
        .box(height, width, thickness)
        .faces(">Z")
        .workplane()
        .hole(diameter)
        .faces(">Z")
        .workplane()
        .rect(height - padding, width - padding, forConstruction=True)
        .vertices()
        .cboreHole(2.4, 4.4, 2.1)
    )
    stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
    cq.exporters.export(result, stl_filename)
    shape = Shape(stl_filename)
    lines, arcs = shape.get_lines_and_arcs()

    assert len(lines) == 1
    assert len(arcs) == 2

    assert len(lines[0]) == 4
    assert len(arcs[0]) == 1
