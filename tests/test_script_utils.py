import random


def distance_to_analog_output(distance: float):
    """
    distance: float in m
    """
    distance = distance * 1000 * 135  # m to mm, distance to analog output
    # add noise
    distance = distance + (distance * 0.001 * (2 * random.random() - 1))
    return round(distance)


def test_distance_to_analog_output():
    distance_in_mm = 10.5
    analog_output = distance_to_analog_output(distance_in_mm / 1000)
    assert analog_output > 0
    assert analog_output < 19000
