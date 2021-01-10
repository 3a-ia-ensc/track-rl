import numpy as np
from termcolor import colored

from src.CarAgent import CarAgent
from src.Track import Track
from src.Vector import Vector
from src.utils import pos2coord


def draw(track, states):
    lstates = []
    for s in states:
        lstates.append(pos2coord(s, track.width))

    pos = track.car.Pos

    height, width = track.shape
    str = ''

    for y in range(height):
        for x in range(width):
            if pos == (x, y) and track[y, x]:
                str += colored('C', 'blue')
            elif pos == (x, y) and not track[y, x]:
                str += colored('£', 'red')
            elif (x, y) in lstates:
                str += colored('@', 'blue')
            elif not track[y, x]:
                str += colored('█', 'grey')
            elif (x, y) in track._finishLine:
                str += colored('▚', 'white')
            elif (x, y) in track._checkpointLine:
                str += colored('▚', 'green')
            else:
                str += ' '

        str += '\n'

    print(str)

track = Track('tracks/track04.png', startPos=Vector(26, 7), finishA=Vector(25, 2), finishB=Vector(25, 14),
              checkPointA=Vector(22, 2), checkPointB=Vector(22, 14))

# draw(track, car)

n_states = track.states
n_actions = 9

Q = np.zeros((n_states, n_actions))

# plus alpha est grand plus on favorise l'exploration
alpha = 0.76
gamma = 0.99

nb_episods = 50000

list_actions = []
list_states = []
cumul_reward = []

for step in range(nb_episods):
    s = track.reset()

    e = False
    mem_actions = []
    mem_states = []
    mem_rewards = []

    while not e:
        # Génération d'un tableau de variables aléatoires
        a = np.random.randint(0, n_actions)
        # On choisit une des actions au hasard
        #a = np.argmax(Q[s, :] + l)

        s1, r, e = track.playAction(a)
        mem_rewards.append(r)
        Q[s, a] = Q[s, a] + alpha * (r + gamma * np.max(Q[s1, :]) - Q[s, a])
        mem_actions.append(a)
        s = s1
        mem_states.append(s)
        #Q[(state, action)] = (1 - alpha) * Q + alpha * (reward + gamma * maxNext)

    list_actions.append(mem_actions)
    list_states.append(mem_states)
    cumul_reward.append(np.sum(mem_rewards))

print(f'Mean score over time: {np.mean(cumul_reward)}')
print(f'Sum score over time: {np.sum(cumul_reward)}')

print(mem_states)
draw(track, mem_states)
