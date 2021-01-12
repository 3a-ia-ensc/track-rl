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


class QLearning:
    def __init__(self, track, alpha=0.1, gamma=0.95):
        self._alpha = alpha
        self._gamma = gamma
        self._track = track

        self._n_states = track.states
        self._n_actions = len(track.actions)

        self._Q = np.zeros((self._n_states, self._n_actions))

        self._list_actions = []
        self._list_states = []
        self._cumul_reward = []

    def run_episode(self):
        """ Run one episode of the Q-Learning algorithm
        """
        s = self._track.reset()
        e = False
        mem_actions = []
        mem_states = []
        mem_rewards = []

        while not e:
            l = np.random.randn(1, self._n_actions)
            a = np.argmax(self._Q[s, :] + l)

            s1, r, e = self._track.playAction(a)
            mem_rewards.append(r)

            self._Q[s, a] = self._Q[s, a] + self._alpha * (r + self._gamma * np.max(self._Q[s1, :]) - self._Q[s, a])

            mem_actions.append(a)
            s = s1
            mem_states.append(s)

        self._list_actions.append(mem_actions)
        self._list_states.append(mem_states)
        self._cumul_reward.append(np.sum(mem_rewards))

    def simulate(self, n_episods):
        """ Run multiple episods of the algorithm

        :param n_episods (int): number of episods to run
        """
        for episod in range(n_episods):
            self.run_episode()
