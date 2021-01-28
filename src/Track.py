# -*- coding: utf-8 -*-

""" Track.py
"""

__author__ = "Simon Audrix and Gabriel Nativel-Fontaine"
__credits__ = ["Simon Audrix", "Gabriel Nativel-Fontaine"]
__copyright__ = "Copyright 2021, Apprentissage par renforcement"
__version__ = "1.0"
__email__ = "gnativ910e@ensc.fr"
__status__ = "Development"

import numpy as np
from PIL import Image

from src.utils import bresenham, coord2pos
from src.CarAgent import CarAgent
from src.Vector import Vector


class Track:
    """ Track object represents the modelisation of our problem
    """
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

        self.actions = []

    def _load(self, path):
        """ Load an image file representing a track in a np.array

        :param path (string): image path
        :return: np.array
        """
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
        """ Compute the next state and rewards for an agent for a given action

        :param action (int): action to perform
        :return: ((int) new state, (float) reward, (bool) is new state terminal)
        """
        self._counter += 1
        new_pos, new_speed = self.car.Move(action)

        end = False
        out, pts = self.outOfTrack(self.car.Pos, new_pos)

        if out:
            r = -100
            new_pos = pts
            new_speed = Vector(0, 0)
        elif self.crossedLine(self.car.Pos, new_pos, self._checkpointLine1):
            if not self._checkpointCrossed[0]:
                r = 20
                self._checkpointCrossed[0] = True
            else:
                r = -20
        elif self.crossedLine(self.car.Pos, new_pos, self._checkpointLine2):
            if self._checkpointCrossed[0] and not self._checkpointCrossed[1]:
                r = 20
                self._checkpointCrossed[1] = True
            else:
                r = -20
        elif self.crossedLine(self.car.Pos, new_pos, self._finishLine):
            if self._checkpointCrossed[0] and self._checkpointCrossed[1]:
                r = 100
                end = True
            else:
                r = -100
        elif new_pos in self.car._path:
            r = -100
        else:
            r = -1

        if self._counter > 200:
            r = -1000
            end = True

        if not end:
            self.car.ComputeMove(new_pos, new_speed)

        return coord2pos(new_pos, self.width), r, end

    def reset(self):
        """ Reset the world

        :return: initial position of the agent
        """
        self.car.Reset(self._startPos)
        self._checkpointCrossed = [False, False]
        self._counter = 0
        return coord2pos(self._startPos, self.width)

    def crossedLine(self, ptsA, ptsB, line):
        """ Determines if a has been crossed

        :param ptsA (Vector): starting vector
        :param ptsB (Vector): arrival vector
        :param line (list): line to check as a list Vector
        :return: bool
        """
        pts = bresenham(ptsA, ptsB)
        for p in pts:
            if p in line: return True

        return False

    def outOfTrack(self, ptsA, ptsB):
        """ Determines if the car got out of track

        :param ptsA (Vector): starting point
        :param ptsB (Vector): arrival point
        :return: bool
        """
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
