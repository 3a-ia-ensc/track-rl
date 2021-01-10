from src.Vector import Vector


def lowLine(ptsA, ptsB):
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
    return vec.y*width + vec.x


def pos2coord(idx, width):
    return Vector(idx%width, idx//width)
