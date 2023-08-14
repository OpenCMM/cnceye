from cnceye.coordinate import Coordinate
import numpy as np
from scipy.optimize import least_squares


class Arc:
    def __init__(self, radius: float, center: Coordinate) -> None:
        self.radius = radius
        self.center = center

    def __repr__(self) -> str:
        return f"Arc(radius={self.radius}, center={self.center})"



def point_id(point: list):
    return f"{point[0]},{point[1]},{point[2]}"


def get_arc_info(arc_points: list):
    """
    Get information about arc

    Parameters
    ----------
    arc_points : list
        List of arc coordinates [(x,y,z), (x,y,z)]

    Returns
    -------
    radius : float
        Radius of arc
    center : np.array
        Center of arc
    """
    center_x, center_y, radius = fit_circle(arc_points[:, :2])
    center = np.array([center_x, center_y, arc_points[0, 2]])
    return radius, center


def circle_residuals(params, x, y):
    cx, cy, r = params
    return (x - cx) ** 2 + (y - cy) ** 2 - r**2


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


def pick_arc_points(arc_points: list):
    """
    Pick 4 points that define the arc
    """
    count = len(arc_points)
    if count < 4:
        raise ValueError("Not enough points to define arc")

    a = arc_points[0]  # first point
    d = arc_points[-1]  # last point

    one_third = count // 3
    b = arc_points[one_third - 1]
    c = arc_points[one_third * 2 - 1]

    return a, b, c, d


def to_arc_list(arc_points: list):
    a, b, c, d = pick_arc_points(arc_points)
    radius, center = get_arc_info(arc_points)
    return [
        point_id(a),
        point_id(b),
        point_id(c),
        point_id(d),
        float(radius),
        float(center[0]),
        float(center[1]),
        float(center[2]),
    ]