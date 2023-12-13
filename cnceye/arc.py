import numpy as np
from scipy.optimize import least_squares


def get_edges_for_arc(arc_points: np.ndarray, number_of_edges: int):
    """
    Returns a list of edges for an arc/circle
    Edges need to be distributed evenly along the arc
    """
    count = len(arc_points)
    if count < 4:
        raise ValueError("Not enough points to define arc")

    if number_of_edges < 3:
        raise ValueError("Not enough edges to define arc")

    interval = count // number_of_edges

    edges = []
    for i in range(number_of_edges):
        x, y, z = arc_points[i * interval].tolist()
        edges.append((round(x, 3), round(y, 3), round(z, 3)))

    return edges


def get_arc_info(arc_points: np.ndarray, decimal_places: int = 3):
    """
    Get information about arc

    Parameters
    ----------
    arc_points : list
        List of arc coordinates [(x,y,z), (x,y,z)]
    decimal_places : int
        Number of decimal places to round to

    Returns
    -------
    radius : float
        Radius of arc
    center : np.array
        Center of arc
    is_circle : bool
        True if arc is a circle
    """
    center_x, center_y, radius = fit_circle(arc_points[:, :2])
    center = np.array([center_x, center_y, arc_points[0, 2]])
    center = np.round(center, decimal_places)
    radius = round(radius, decimal_places)
    return radius, center, is_circle(arc_points)


def fit_circle(points):
    x = points[:, 0]
    y = points[:, 1]

    initial_params = (
        np.mean(x),
        np.mean(y),
        np.std(np.sqrt((x - np.mean(x)) ** 2 + (y - np.mean(y)) ** 2)),
    )

    result = least_squares(circle_residuals, initial_params, args=(x, y))
    cx, cy, r = result.x

    return cx, cy, r


def circle_residuals(params, x, y):
    cx, cy, r = params
    return (x - cx) ** 2 + (y - cy) ** 2 - r**2


def is_circle(points, tolerance=1.0):
    """
    Check if points are a circle within a tolerance

    If they are a circle, distances between points should be within tolerance.
    If not, they are an arc.
    """
    x = points[:, 0]
    y = points[:, 1]
    distances = np.sqrt((x - np.mean(x)) ** 2 + (y - np.mean(y)) ** 2)
    return np.allclose(distances, distances[0], atol=tolerance)
