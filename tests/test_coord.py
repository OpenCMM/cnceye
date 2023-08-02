from cnceye.coordinate import Coordinate


def test_coordinate():
    coord = Coordinate(1.0, 2.0, 3.0)
    assert coord.x == 1.0
    assert coord.y == 2.0
    assert coord.z == 3.0


def test_add_coordinate():
    coord1 = Coordinate(1.0, 2.0, 3.0)
    coord2 = Coordinate(4.0, 5.0, 6.0)
    coord3 = coord1 + coord2
    assert coord3.x == 5.0
    assert coord3.y == 7.0
    assert coord3.z == 9.0


def test_sub_coordinate():
    coord1 = Coordinate(1.0, 2.0, 3.0)
    coord2 = Coordinate(4.0, 5.0, 6.0)
    coord3 = coord1 - coord2
    assert coord3.x == -3.0
    assert coord3.y == -3.0
    assert coord3.z == -3.0


def test_mul_coordinate():
    coord1 = Coordinate(1.0, 2.0, 3.0)
    coord2 = Coordinate(4.0, 5.0, 6.0)
    coord3 = coord1 * coord2
    assert coord3.x == 4.0
    assert coord3.y == 10.0
    assert coord3.z == 18.0


def test_div_coordinate():
    coord1 = Coordinate(1.0, 2.0, 3.0)
    coord2 = Coordinate(4.0, 5.0, 6.0)
    coord3 = coord1 / coord2
    assert coord3.x == 0.25
    assert coord3.y == 0.4
    assert coord3.z == 0.5


def test_distance_to():
    coord1 = Coordinate(1.0, 2.0, 3.0)
    coord2 = Coordinate(1.0, 5.0, 3.0)
    coord3 = Coordinate(4.0, 5.0, 6.0)

    assert coord1.distance_to(coord2) == 3.0
    assert coord1.distance_to(coord3) == 5.196152422706632
