import cv2


def get_circles(
    image,
    min_dist: int,
    param2: int,
    min_radius: int,
    max_radius: int,
):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detect circles in the image
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        1.5,
        min_dist,
        None,
        200,
        param2,
        min_radius,
        max_radius,
    )
    return circles
