from cnceye.edge import find


def test_find_edge():
    filepath = "tests/fixtures/sensor/one_edge.csv"
    edge_position = find.find_edge(filepath)
    print(edge_position)


def test_find_edge_from_sqlite():
    db_path = "tests/fixtures/db/listener.db"
    edges = find.find_edges_from_sqlite(db_path, 100.0)
    print(edges)
    assert len(edges) == 16


def test_check_if_edge_is_found():
    assert find.check_if_edge_is_found("", "") is False
    assert find.check_if_edge_is_found("", 100.0) is True
    assert find.check_if_edge_is_found(100.0, "") is True
    assert find.check_if_edge_is_found(100.0, 99.9) is False
    assert find.check_if_edge_is_found(100.0, 50.0) is True
    assert find.check_if_edge_is_found(50.0, 100.0) is True
    assert find.check_if_edge_is_found(99.9, 100.0) is False
    assert find.check_if_edge_is_found(99.0, 100.0, 0.1) is True


def test_find_line():
    filepath = "tests/fixtures/sensor/line.csv"
    lines = find.find_lines(filepath, 3)
    assert len(lines) == 1
    line = lines[0]
    expected_x = 50.0
    for row in line:
        x = float(row[0])
        assert x == expected_x


def test_find_lines():
    filepath = "tests/fixtures/sensor/lines.csv"
    lines = find.find_lines(filepath, 3)
    assert len(lines) == 4
    for line in lines:
        print(line)
