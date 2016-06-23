from __future__ import division

import numpy as np
import random

from collections import defaultdict
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator


class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.q_table = []
        self.q = 0.0
        self.state = ''
        self.total_reward = 0
        self.trial_count = 0

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.q = 0.0#Not sure about this here
        self.state = ''
        self.total_reward = 0
        self.trial_count += 1

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = [i for i in inputs.iteritems()]
        self.state.append(self.next_waypoint)

        # TODO: Select action according to your policy
        temp_list = []
        if self.q_table == []:
            action = self.next_waypoint
        else:
            for i in self.q_table:
                if i[0] == self.state:
                    temp_list.append((i[0][-1], i[1:]))

                if temp_list == []:
                    action = self.next_waypoint
                else:
                    max_action = max(temp_list, key=lambda x: x[0][1][0])[0]
                    action = max_action
  

        # Execute action and get reward
        reward = self.env.act(self, action)
        self.total_reward += reward

        # TODO: Learn policy based on state, action, reward
        if self.q_table == []:
            alpha = 1
            gamma = 1
            self.q += self.q + alpha * (reward + gamma * 0 - self.q)
        else:
            alpha = 1 / len(self.q_table)
            gamma = 1 / len(self.q_table)
            #Tempory list to hold similar states
            if self.q_table == []:
                max_q = [0]
            else:
                max_q = []

            #Loop through q_table to get all rewards for identical state/action pairs
            for i in self.q_table:
                if i[0] == self.state:
                    max_q.append(i[2])

            if max_q == []:
                max_q = [0]

            self.q += self.q + alpha * (reward + gamma * np.max(max_q) - self.q)

        self.q_table.append((self.state, reward, self.q))

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}, total reward = {}".format(
                        deadline, inputs, action, reward, self.total_reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=.1)  # reduce update_delay to speed up simulation
    sim.run(n_trials=100)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
