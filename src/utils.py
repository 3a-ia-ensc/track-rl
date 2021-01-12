# -*- coding: utf-8 -*-

""" utils.py
This module contains some useful functions
"""

__author__ = "Simon Audrix and Gabriel Nativel-Fontaine"
__credits__ = ["Simon Audrix", "Gabriel Nativel-Fontaine"]
__copyright__ = "Copyright 2021, Apprentissage par renforcement"
__version__ = "2.0.0"
__email__ = "gnativ910e@ensc.fr"
__status__ = "Development"


from src.Vector import Vector


def lowLine(ptsA, ptsB):
    """ Lower part of bresenham algorithm

    :param ptsA:
    :param ptsB:
    :return:
    """
    pts = [ptsA]
    x1, y1 = ptsA.x, ptsA.y
    x2, y2 = ptsB.x, ptsB.y

    dx = x2 - x1
    dy = y2 - y1
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy

    error = (2*dy) - dx
    y = y1

    for x in range(x1, x2):
        pts.append(Vector(x, y))
        if error > 0:
            y += yi
            error += 2 * (dy-dx)
        else:
            error += 2 * dy

    pts.append(ptsB)
    return pts


def highLine(ptsA, ptsB):
    """ Upper part of bresenham algorithm

    :param ptsA:
    :param ptsB:
    :return:
    """
    pts = [ptsA]
    x1, y1 = ptsA.x, ptsA.y
    x2, y2 = ptsB.x, ptsB.y

    dx = x2 - x1
    dy = y2 - y1
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx

    error = (2 * dx) - dy
    x = x1

    for y in range(y1, y2):
        pts.append(Vector(x, y))
        if error > 0:
            x += xi
            error += 2 * (dx - dy)
        else:
            error += 2 * dx

    pts.append(ptsB)
    return pts


def bresenham(ptsA, ptsB):
    """ Computes a line with bresenham algorithm

    :param ptsA:
    :param ptsB:
    :return:
    """
    x1, y1 = ptsA.x, ptsA.y
    x2, y2 = ptsB.x, ptsB.y

    if abs(y2 - y1) < abs(x2 - x1):
        if x1 > x2:
            return lowLine(ptsB, ptsA)
        else:
            return lowLine(ptsA, ptsB)
    else:
        if y1 > y2:
            return highLine(ptsB, ptsA)
        else:
            return highLine(ptsA, ptsB)


def coord2pos(vec, width):
    """ Convert coordinate to position

    :param vec (Vector): Vector to convert
    :param width (int): Width of the world
    :return: (int) Position
    """
    return vec.y*width + vec.x


def pos2coord(idx, width):
    """ Convert position to coordinates

    :param idx (int): position to convert
    :param width: world's width
    :return: (x, y) coordinates
    """
    return Vector(idx%width, idx//width)
