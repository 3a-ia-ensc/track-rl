from src.CarAgent import CarAgent
from src.Track import Track

from termcolor import colored
import numpy as np

from src.Vector import Vector


def lowLine(ptsA, ptsB):
    pts = [ptsA, ptsB]
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

    return pts


def highLine(ptsA, ptsB):
    pts = [ptsA, ptsB]
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


def draw(track, car):
    pos = car.NextPossibleMove()

    height, width = track.shape
    str = ''

    finishLine = bresenham(track.finishA, track.finishB)
    checkpointLine = bresenham(track.checkPointA, track.checkPointB)

    for y in range(height):
        for x in range(width):
            if car.Pos == (x, y) and track[y, x]:
                str += colored('C', 'blue')
            elif car.Pos == (x, y) and not track[y, x]:
                str += colored('£', 'red')
            elif not track[y, x]:
                str += colored('█', 'grey')
            elif (x, y) in pos:
                str += colored('*', 'yellow')
            elif (x, y) in finishLine:
                str += colored('▚', 'white')
            elif (x, y) in checkpointLine:
                str += colored('▚', 'green')
            else:
                str += ' '

        str += '\n'

    print(str)

def crossedLine(ptsA, ptsB, line):
    pts = bresenham(ptsA, ptsB)
    for p in pts:
        if p in line: return True

    return False


def outOfTrack(ptsA, ptsB, track):
    pts = bresenham(ptsA, ptsB)
    for p in pts:
        if not track[p.y, p.x]: return True

    return False



if __name__ == '__main__':
    track = Track('tracks/track04.png', Vector(25, 2), Vector(25, 14), Vector(75, 2), Vector(75, 14))
    car = CarAgent(Vector(26, 7))
    draw(track, car)

    finishLine = bresenham(track.finishA, track.finishB)
    checkpointLine = bresenham(track.checkPointA, track.checkPointB)

    for i in range(10):
        prevPos = car.Pos
        car.ComputeMove(8)
        if crossedLine(prevPos, car.Pos, finishLine):
            print('You win !')
        if crossedLine(prevPos, car.Pos, checkpointLine):
            print('Checkpoint ok !')
        if outOfTrack(prevPos, car.Pos, track):
            print('Ouch')
        draw(track, car)



