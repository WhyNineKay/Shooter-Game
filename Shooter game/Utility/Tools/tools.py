import random
from typing import Tuple
import math
import pygame.rect

from Utility import globs


def true_or_false():
    return random.randint(0, 1) == 1


def random_angle(use_float: bool = False) -> float | int:
    """
    Returns a random angle between 0 and 360 degrees.
    :return:
    """
    if use_float:
        return random.uniform(0, 360)
    else:
        return random.randint(0, 360)


def to_grey_scale(color: tuple[int, int, int]):
    # Get average of RGB values
    avg = (color[0] + color[1] + color[2]) // 3
    color = (avg, avg, avg)
    return color


def random_color_from_range(start: tuple[int, int, int], end: tuple[int, int, int], *, to_grayscale: bool = False) -> tuple[int, int, int]:
    """
    Returns a random color from a range of colors.
    :param to_grayscale:
    :param start:
    :param end:
    :return:
    """

    r = random.randint(start[0], end[0]) if start[0] <= end[0] else random.randint(end[0], start[0])
    g = random.randint(start[1], end[1]) if start[1] <= end[1] else random.randint(end[1], start[1])
    b = random.randint(start[2], end[2]) if start[2] <= end[2] else random.randint(end[2], start[2])

    if to_grayscale:
        return to_grey_scale((r, g, b))

    return (r, g, b)


def random_vibrant_rgb(*, range_start=200, range_end=255) -> tuple[int, int, int]:
    """
    Returns a random color from a range of colors that are vibrant.
    :return:
    """
    color = [0, 0, 0]

    first_color = random.randint(1, 3)
    second_color = random.randint(1, 3)

    for i in range(3):
        if first_color == i + 1:
            color[i] = random.randint(range_start, range_end)
            break

    for i in range(3):
        if second_color == i + 1:
            color[i] = random.randint(range_start, range_end)
            break

    color = tuple(color)

    return color


def get_distance(Rect1: pygame.rect.Rect, Rect2: pygame.rect.Rect) -> float:
    """
    Returns the distance between two rectangles.
    :param Rect1:
    :param Rect2:
    :return:
    """
    return ((Rect1.x - Rect2.x) ** 2 + (Rect1.y - Rect2.y) ** 2) ** 0.5

def get_angle(Rect1: pygame.rect.Rect, Rect2: pygame.rect.Rect) -> float:
    """
    Returns the angle between two rectangles.
    :param Rect1:
    :param Rect2:
    :return:
    """
    angle = math.degrees(math.atan2(Rect1.y - Rect2.y, Rect1.x - Rect2.x))

    if angle > 180:
        angle = 360 - angle

    return angle

def collides_with_wall(Rect: pygame.rect.Rect) -> bool:
    """
    Checks if a rectangle collides with any of the walls.
    :param Rect:
    :return:
    """
    for wall in globs.walls:
        if Rect.colliderect(wall):
            return True

    return False


def distance_between_points(ax, ay, bx, by) -> float:
    """
    Returns the distance between two points.
    :param ax:
    :param ay:
    :param bx:
    :param by:
    :return:
    """
    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5
