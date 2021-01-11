from src.Vector import Vector


class CarAgent:
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

    def Reset(self, pos):
        self._pos = pos
        self._speed = Vector(0, 0)
        self._path = []

    def ComputeMove(self, pos, speed):
        self._pos = pos
        self._speed = speed
        self._path.append(pos)

    def Move(self, action):
        pos = self._acceleration[action] + self._speed + self._pos
        speed = self._speed + self._acceleration[action] * self._power
        return pos, speed

    def NextPossibleMove(self):
        possiblePos = []
        for a in self._acceleration:
            pos = a + self._speed + self._pos
            possiblePos.append(pos)

        return possiblePos


