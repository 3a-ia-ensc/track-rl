import numpy as np
from termcolor import colored
from tqdm import tqdm

from src.CarAgent import CarAgent
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

track = Track('tracks/track05.png', startPos=Vector(26, 3), finishA=Vector(25, 1), finishB=Vector(25, 5),
              checkPointC=Vector(20, 44), checkPointD=Vector(20, 48),
              checkPointA=Vector(89, 8), checkPointB=Vector(99, 8))
print(track.shape)
draw(track)

n_states = track.states
n_actions = 9

Q = np.zeros((n_states, n_actions))

alpha = 0.2
gamma = 0.6

nb_episods = 150000

list_actions = []
list_states = []
cumul_reward = []

for step in tqdm(range(nb_episods)):
    s = track.reset()
    e = False
    mem_actions = []
    mem_states = []
    mem_rewards = []

    while not e:
        # Génération d'un tableau de variables aléatoires
        l = np.random.randn(1, n_actions)
        # On choisit une des actions au hasard
        a = np.argmax(Q[s, :] + l)

        s1, r, e = track.playAction(a)
        mem_rewards.append(r)
        if s1 > 5000:
            print(s1)

        Q[s, a] = Q[s, a] + alpha * (r + gamma * np.max(Q[s1, :]) - Q[s, a])

        mem_actions.append(a)
        s = s1
        mem_states.append(s)

    list_actions.append(mem_actions)
    list_states.append(mem_states)
    cumul_reward.append(np.sum(mem_rewards))

    if step % 10000 == 0:
        print(mem_states)
        print(mem_actions)
        draw(track, mem_states)


print(f'Mean score over time: {np.mean(cumul_reward)}')
print(f'Sum score over time: {np.sum(cumul_reward)}')
print(f'Length: {len(mem_actions)}')
print(f'Rewards last: {np.sum(mem_rewards)}')

print(mem_states)
print(mem_actions)
draw(track, mem_states)
