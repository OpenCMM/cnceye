from cnceye import Shape
import cadquery as cq
import pytest


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
    for arc_points in arcs[0]:
        radius, center, is_circle = shape.get_arc_info(arc_points)
        # assert is_circle is True
        print(radius, center, is_circle)
        assert radius == 5 or radius == 9


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
    small_hole_diameter = 4.4

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
        .cboreHole(2.4, small_hole_diameter, 2.1)
    )
    stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
    cq.exporters.export(result, stl_filename)
    shape = Shape(stl_filename)
    lines, arcs = shape.get_lines_and_arcs()
    assert len(lines) == 1
    assert len(arcs) == 2
    assert len(lines[0]) == 4
    assert len(arcs[0]) == 5
    assert len(arcs[1]) == 8

    for arc_points in arcs[0]:
        radius, center, is_circle = shape.get_arc_info(arc_points)
        # assert is_circle is True
        print(radius, center, is_circle)
        assert radius == small_hole_diameter / 2 or radius == diameter / 2


def test_group_by_common_point_cadquery_models_filleting():
    height = 60.0
    width = 80.0
    thickness = 10.0
    diameter = 22.0
    padding = 12.0
    small_hole_diameter = 4.4

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
        .cboreHole(2.4, small_hole_diameter, 2.1)
        .edges("|Z")
        .fillet(2.0)
    )
    stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
    cq.exporters.export(result, stl_filename)
    shape = Shape(stl_filename)
    shapes = shape.get_shapes()
    point_groups = shape.group_by_common_point(shapes[0])
    assert len(point_groups) == 6
    point_groups = shape.group_by_common_point(shapes[1])
    assert len(point_groups) == 8


def test_cadquery_models_filleting():
    height = 60.0
    width = 80.0
    thickness = 10.0
    diameter = 22.0
    padding = 12.0
    small_hole_diameter = 4.4

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
        .cboreHole(2.4, small_hole_diameter, 2.1)
        .edges("|Z")
        .fillet(2.0)
    )
    stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
    cq.exporters.export(result, stl_filename)
    shape = Shape(stl_filename)
    lines, arcs = shape.get_lines_and_arcs()
    assert len(lines) == 1
    assert len(arcs) == 2
    assert len(lines[0]) == 4
    assert len(arcs[0]) == 9
    assert len(arcs[1]) == 8

    for arc_points in arcs[0]:
        radius, center, is_circle = shape.get_arc_info(arc_points)
        # assert is_circle is True
        print(radius, center, is_circle)
        # assert radius == small_hole_diameter / 2 or radius == diameter / 2


def test_group_by_common_point():
    height = 20.0
    width = 30.0
    thickness = 10.0
    radius = 82.0

    result = cq.Workplane("front").circle(radius).rect(height, width).extrude(thickness)

    stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
    cq.exporters.export(result, stl_filename)
    shape = Shape(stl_filename)
    shapes = shape.get_shapes()
    point_groups = shape.group_by_common_point(shapes[0])
    assert len(point_groups) == 2
    assert len(point_groups[0]) == 127
    assert len(point_groups[1]) == 5


def test_group_by_common_point_with_line_and_arc():
    shape = Shape("tests/fixtures/stl/sample.stl")
    shapes = shape.get_shapes()
    point_groups = shape.group_by_common_point(shapes[0])
    assert len(point_groups) == 3


def test_cadquery_model_rectangle_inside_circle():
    height = 20.0
    width = 30.0
    thickness = 10.0
    radius = 82.0

    result = cq.Workplane("front").circle(radius).rect(height, width).extrude(thickness)

    stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
    cq.exporters.export(result, stl_filename)
    shape = Shape(stl_filename)
    lines, arcs = shape.get_lines_and_arcs()
    assert len(lines) == 1
    assert len(arcs) == 1
    assert len(lines[0]) == 4
    assert len(arcs[0]) == 1

    for arc_points in arcs[0]:
        _radius, center, is_circle = shape.get_arc_info(arc_points)
        # assert is_circle is True
        assert radius == _radius


def test_with_a_large_model():
    height = 200.0
    width = 300.0
    thickness = 100.0
    radius = 802.0

    result = cq.Workplane("front").circle(radius).rect(height, width).extrude(thickness)

    stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
    cq.exporters.export(result, stl_filename)
    shape = Shape(stl_filename)
    lines, arcs = shape.get_lines_and_arcs()
    assert len(lines) == 1
    assert len(arcs) == 1
    assert len(lines[0]) == 4
    assert len(arcs[0]) == 1

    for arc_points in arcs[0]:
        _radius, center, is_circle = shape.get_arc_info(arc_points)
        # assert is_circle is True
        assert radius == _radius


def test_with_a_small_model():
    height = 0.02
    width = 0.03
    thickness = 0.1
    radius = 0.8

    result = cq.Workplane("front").circle(radius).rect(height, width).extrude(thickness)

    stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
    cq.exporters.export(result, stl_filename)
    shape = Shape(stl_filename)
    lines, arcs = shape.get_lines_and_arcs()
    assert len(lines) == 1
    assert len(arcs) == 1
    assert len(lines[0]) == 4
    assert len(arcs[0]) == 1

    for arc_points in arcs[0]:
        _radius, center, is_circle = shape.get_arc_info(arc_points)
        # assert is_circle is True
        assert radius == _radius


def test_with_a_prismatic_solid():
    result = (
        cq.Workplane("front")
        .lineTo(2.0, 0)
        .lineTo(2.0, 1.0)
        .threePointArc((1.0, 1.5), (0.0, 1.0))
        .close()
        .extrude(0.25)
    )

    stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
    cq.exporters.export(result, stl_filename)
    shape = Shape(stl_filename)
    lines, arcs = shape.get_lines_and_arcs()
    assert len(lines) == 1
    assert len(arcs) == 1
    assert len(lines[0]) == 3
    assert len(arcs[0]) == 1

    for arc_points in arcs[0]:
        _radius, center, is_circle = shape.get_arc_info(arc_points)
        print(_radius, center, is_circle)


def test_multiple_holes_inside_circle():
    result = cq.Workplane("front").circle(
        3.0
    )  # current point is the center of the circle, at (0, 0)
    result = result.center(1.5, 0.0).rect(0.5, 0.5)  # new work center is (1.5, 0.0)

    result = result.center(-1.5, 1.5).circle(0.25)  # new work center is (0.0, 1.5).
    # The new center is specified relative to the previous center, not global coordinates!

    result = result.extrude(0.25)

    stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
    cq.exporters.export(result, stl_filename)
    shape = Shape(stl_filename)
    lines, arcs = shape.get_lines_and_arcs()
    assert len(lines) == 1
    assert len(arcs) == 1
    assert len(lines[0]) == 4
    assert len(arcs[0]) == 2

    for arc_points in arcs[0]:
        _radius, center, is_circle = shape.get_arc_info(arc_points)
        print(_radius, center, is_circle)


def test_using_join_list():
    r = cq.Workplane("front").circle(2.0)  # make base
    r = r.pushPoints(
        [(1.5, 0), (0, 1.5), (-1.5, 0), (0, -1.5)]
    )  # now four points are on the stack
    r = r.circle(0.25)  # circle will operate on all four points
    result = r.extrude(0.125)  # make prism

    stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
    cq.exporters.export(result, stl_filename)
    shape = Shape(stl_filename)
    lines, arcs = shape.get_lines_and_arcs()
    assert len(lines) == 0
    assert len(arcs) == 1
    assert len(arcs[0]) == 5

    for arc_points in arcs[0]:
        _radius, center, is_circle = shape.get_arc_info(arc_points)
        print(_radius, center, is_circle)


def test_polygons():
    result = (
        cq.Workplane("front")
        .box(3.0, 4.0, 0.25)
        .pushPoints([(0, 0.75), (0, -0.75)])
        .polygon(6, 1.0)
        .cutThruAll()
    )

    stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
    cq.exporters.export(result, stl_filename)
    shape = Shape(stl_filename)
    lines, arcs = shape.get_lines_and_arcs()
    assert len(lines) == 1
    assert len(arcs) == 0
    assert len(lines[0]) == 16


def test_polylines():
    (L, H, W, t) = (100.0, 20.0, 20.0, 1.0)
    pts = [
        (0, H / 2.0),
        (W / 2.0, H / 2.0),
        (W / 2.0, (H / 2.0 - t)),
        (t / 2.0, (H / 2.0 - t)),
        (t / 2.0, (t - H / 2.0)),
        (W / 2.0, (t - H / 2.0)),
        (W / 2.0, H / -2.0),
        (0, H / -2.0),
    ]
    result = cq.Workplane("front").polyline(pts).mirrorY().extrude(L)

    stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
    cq.exporters.export(result, stl_filename)
    shape = Shape(stl_filename)
    lines, arcs = shape.get_lines_and_arcs()
    assert len(lines) == 1
    assert len(arcs) == 0
    assert len(lines[0]) == 12


@pytest.mark.skip(reason="Not implemented yet")
def test_spline():
    s = cq.Workplane("XY")
    sPnts = [
        (2.75, 1.5),
        (2.5, 1.75),
        (2.0, 1.5),
        (1.5, 1.0),
        (1.0, 1.25),
        (0.5, 1.0),
        (0, 1.0),
    ]
    r = s.lineTo(3.0, 0).lineTo(3.0, 1.0).spline(sPnts, includeCurrent=True).close()
    result = r.extrude(0.5)

    stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
    cq.exporters.export(result, stl_filename)
    shape = Shape(stl_filename)
    lines, arcs = shape.get_lines_and_arcs()
    assert len(lines) == 1
    assert len(arcs) > 0
    assert len(lines[0]) == 3


def test_mirror_2D_geometry():
    r = cq.Workplane("front").hLine(1.0)  # 1.0 is the distance, not coordinate
    r = (
        r.vLine(0.5).hLine(-0.25).vLine(-0.25).hLineTo(0.0)
    )  # hLineTo allows using xCoordinate not distance
    result = r.mirrorY().extrude(0.25)  # mirror the geometry and extrude

    stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
    cq.exporters.export(result, stl_filename)
    shape = Shape(stl_filename)
    lines, arcs = shape.get_lines_and_arcs()
    assert len(lines) == 1
    assert len(arcs) == 0
    assert len(lines[0]) == 8


def test_mirror_from_faces():
    result = cq.Workplane("XY").line(0, 1).line(1, 0).line(0, -0.5).close().extrude(1)
    result = result.mirror(result.faces(">X"), union=True)

    stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
    cq.exporters.export(result, stl_filename)
    shape = Shape(stl_filename)
    lines, arcs = shape.get_lines_and_arcs()
    assert len(lines) == 1
    assert len(arcs) == 0
    assert len(lines[0]) == 5


# def test_cut_a_corner_out():
#     result = cq.Workplane("front").box(10, 6, 2.0)  # make a basic prism
#     result = (
#         result.faces(">Z").vertices("<XY").workplane(centerOption="CenterOfMass")
#     )  # select the lower left vertex and make a workplane
#     result = result.circle(1.0).cutThruAll()  # cut the corner out

#     stl_filename = "tests/fixtures/stl/cq/cadquery_model.stl"
#     cq.exporters.export(result, stl_filename)
#     shape = Shape(stl_filename)
#     lines, arcs = shape.get_lines_and_arcs()
#     assert len(lines) == 1
#     assert len(arcs) == 1
#     assert len(lines[0]) == 4
#     assert len(arcs[0]) == 1
