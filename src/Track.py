import numpy as np
from PIL import Image

from src.utils import bresenham, coord2pos
from src.CarAgent import CarAgent
from src.Vector import Vector


class Track:
    def __init__(self, path, startPos, finishA, finishB, checkPointA, checkPointB, checkPointC, checkPointD):
        self._track = self._load(path)
        self._finishVector = finishB - finishA
        self.finishA = finishA
        self.finishB = finishB

        self.checkPointA = checkPointA
        self.checkPointB = checkPointB

        self._finishLine = bresenham(finishA, finishB)
        self._checkpointLine1 = bresenham(checkPointA, checkPointB)
        self._checkpointLine2 = bresenham(checkPointC, checkPointD)

        self._startPos = startPos
        self.car = CarAgent(startPos)
        self._checkpointCrossed = [False, False]
        self._counter = 0

    def _load(self, path):
        arr = np.sum(np.asarray(Image.open(path)), axis=2) == 255 * 3
        return arr

    @property
    def states(self):
        return self.width * self.height

    @property
    def shape(self):
        return self._track.shape

    @property
    def width(self):
        return self.shape[1]

    @property
    def height(self):
        return self.shape[0]

    def playAction(self, action):
        self._counter += 1
        new_pos, new_speed = self.car.Move(action)

        end = False
        out, pts = self.outOfTrack(self.car.Pos, new_pos)

        if out:
            r = -100
            new_pos = pts
            new_speed = Vector(0, 0)
            #end = True
        elif self.crossedLine(self.car.Pos, new_pos, self._checkpointLine1) and not self._checkpointCrossed[0]:
            r = 50
            self._checkpointCrossed[0] = True
            #print('C1')
        elif self.crossedLine(self.car.Pos, new_pos, self._checkpointLine2) and self._checkpointCrossed[0] and not self._checkpointCrossed[1]:
            r = 20
            self._checkpointCrossed[1] = True
            #print('C2')
        elif self.crossedLine(self.car.Pos, new_pos, self._finishLine) and self._checkpointCrossed[0] and self._checkpointCrossed[1]:
            r = 100
            end = True
            print('FINISH')
        elif new_pos in self.car._path:
            r = -100
        else:
            r = -1

        if self._counter > 85:
            r = -1000
            end = True

        if not end:
            self.car.ComputeMove(new_pos, new_speed)

        return coord2pos(new_pos, self.width), r, end


    """def playAction(self, action):
        self._counter += 1
        new_pos, new_speed = self.car.Move(action)

        end = False
        out, pts = self.outOfTrack(self.car.Pos, new_pos) 

        if out:
            r = -10
            new_pos = pts
            new_speed = Vector(0, 0)
            # end = True
        elif self.crossedLine(self.car.Pos, new_pos, self._finishLine):
            if self._checkpointCrossed[0] and self._checkpointCrossed[1]:
                r = 2000
                end = True
            else:
                r = -2000
        elif self.crossedLine(self.car.Pos, new_pos, self._checkpointLine1):
            r = 20
            self._checkpointCrossed[0] = True
        elif self.crossedLine(self.car.Pos, new_pos, self._checkpointLine2):
            r = 20
            if self._checkpointCrossed[0]:
                self._checkpointCrossed[1] = True
        else:
            if new_pos == self.car.Pos:
                r = -100
            else:
                if new_speed.norm() > self.car.Pos.norm():
                    r = -1
                else:
                    r = -2
        if self._counter > 500:
            r = -10
            end = True

        if not end:
            self.car.ComputeMove(new_pos, new_speed)

        return coord2pos(new_pos, self.width), r, end"""

    def reset(self):
        self.car.Reset(self._startPos)
        self._checkpointCrossed = [False, False]
        self._counter = 0
        return coord2pos(self._startPos, self.width)

    def crossedLine(self, ptsA, ptsB, line):
        pts = bresenham(ptsA, ptsB)
        for p in pts:
            if p in line: return True

        return False

    def outOfTrack(self, ptsA, ptsB):
        pts = bresenham(ptsA, ptsB)

        outOfRange = lambda x, y: x < 0 or x >= self.width or y < 0 or y >= self.height

        last = ptsA
        for p in pts:
            if outOfRange(p.x, p.y) or not self._track[p.y, p.x]:
                return True, last
            else:
                last = p

        return False, ptsB

    def __getitem__(self, tup):
        line, col = tup
        return self._track[line, col]

    def __repr__(self):
        return f'Track {self._track.shape}'

    def __str__(self):
        str = ''
        for line in self._track:
            for c in line:
                if c:
                    str += ' '
                else:
                    str += '#'

            str += '\n'

        return str
