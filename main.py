from termcolor import colored

from src.Track import Track
from src.Vector import Vector
from src.utils import pos2coord


def draw(track, states=[]):
    lstates = []
    for s in states:
        lstates.append(pos2coord(s, track.width))

    pos = track.car.Pos

    height, width = track.shape
    str = ''

    stp = 0

    for y in range(height):
        for x in range(width):
            if pos == (x, y) and track[y, x]:
                str += colored('C', 'blue')
            elif pos == (x, y) and not track[y, x]:
                str += colored('£', 'red')
            elif (x, y) in lstates:
                stp += 1
                str += colored(stp%10, 'blue')
            elif not track[y, x]:
                str += colored('█', 'grey')
            elif (x, y) in track._finishLine:
                str += colored('▚', 'white')
            elif (x, y) in track._checkpointLine1:
                str += colored('▚', 'green')
            elif (x, y) in track._checkpointLine2:
                str += colored('▚', 'red')
            else:
                str += ' '

        str += '\n'

    print(str)

if __name__ == '__main__':
    track = Track('tracks/track05.png', startPos=Vector(26, 3), finishA=Vector(25, 1), finishB=Vector(25, 5),
                  checkPointC=Vector(20, 44), checkPointD=Vector(20, 48),
                  checkPointA=Vector(89, 8), checkPointB=Vector(99, 8))


