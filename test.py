# -*- coding: utf-8 -*-

""" qlearning.py
Compute the Q-Learning algorithm
"""

__author__ = "Simon Audrix and Gabriel Nativel-Fontaine"
__credits__ = ["Simon Audrix", "Gabriel Nativel-Fontaine"]
__copyright__ = "Copyright 2021, Apprentissage par renforcement"
__version__ = "2.0"
__email__ = "gnativ910e@ensc.fr"
__status__ = "Development"

import numpy as np
from tqdm import tqdm


class QLearning:
    def __init__(self, alpha, gamma, track):
        self._alpha = alpha
        self._gamma = gamma
        self._track = track

        list_actions = []
        list_states = []
        cumul_reward = []


def qlearning_search(track):
    """ Compute Q-Learning algorithm

    :param track (Track):
    :return:
    """
    n_states = track.states
    n_actions = 9

    Q = np.zeros((n_states, n_actions))

    alpha = 0.1
    gamma = 0.95

    nb_episods = 40000

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
