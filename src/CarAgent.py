# -*- coding: utf-8 -*-

""" CarAgent.py
"""

__author__ = "Simon Audrix and Gabriel Nativel-Fontaine"
__credits__ = ["Simon Audrix", "Gabriel Nativel-Fontaine"]
__copyright__ = "Copyright 2021, Apprentissage par renforcement"
__version__ = "2.0"
__email__ = "gnativ910e@ensc.fr"
__status__ = "Development"


from src.Vector import Vector


class CarAgent:
    """ Car object used to compute the agent movements
    """
    def __init__(self, initPos, power=1):
        self._speed = Vector(0, 0)
        self._acceleration = Vector(0, 0)
        self._pos = initPos
        self._path = []

        self._power = power

        self._acceleration = [
            Vector(-1, -1), Vector(0, -1), Vector(1, -1),
            Vector(-1, 0), Vector(0, 0), Vector(1, 0),
            Vector(-1, 1), Vector(0, 1), Vector(1, 1),
        ]

    @property
    def Pos(self):
        return self._pos

    @property
    def Path(self):
        return self._path

    def Reset(self, pos):
        """ Reset the agent on a given position

        :param pos (Vector): Vector representing the initial position of the agent
        :return:
        """
        self._pos = pos
        self._speed = Vector(0, 0)
        self._path = []

    def ComputeMove(self, pos, speed):
        """ Store the given move

        :param pos (Vector): position vector
        :param speed (Vector): speed vector
        """
        self._pos = pos
        self._speed = speed
        self._path.append(pos)

    def Move(self, action):
        """ Compute position and speed that the agent will have when performing a given move

        :param action (int): move to perform
        :return: (position, speed)
        """
        pos = self._acceleration[action] + self._speed + self._pos
        speed = self._speed + self._acceleration[action] * self._power
        return pos, speed

    def NextPossibleMove(self):
        """ Gives the next 9 positions that the agent will be able to have
        """
        possiblePos = []
        for a in self._acceleration:
            pos = a + self._speed + self._pos
            possiblePos.append(pos)

        return possiblePos
