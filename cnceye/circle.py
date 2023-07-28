import cv2


def get_circles(
    image,
    min_dist: int = 100,
    param2: int = 200,
    min_radius: int = 100,
    max_radius: int = 200,
):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detect circles in the image
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        1.2,
        min_dist,
        None,
        200,
        param2,
        min_radius,
        max_radius,
    )
    return circles
