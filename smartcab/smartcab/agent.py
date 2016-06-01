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

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.q_table = [] #<- this is most likely wrong, reason being the agent has to learn from scratch again.
        self.q = 0.0

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        state = [i for i in inputs.iteritems()]

        # TODO: Select action according to your policy
        action = self.next_waypoint
        state.extend((action, deadline))# Remove deadline, at least for the initial notions of state


        # Execute action and get reward
        reward = self.env.act(self, action)
        self.q_table.append(state)

        # TODO: Learn policy based on state, action, reward
        R = reward #Remove
        gamma = 0.0
        alpha = 0.0
        self.q += self.q + alpha * (reward +((gamma*np.max(no_idea_how_to_do_this) 
            - self.q))) #not sure if self.q is the correct q to subtract here.
        # Q(s,a) = (1-alpha)Q(s,a) + alpha(R + gamma*Q(s`,a`)

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=False)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=1.0)  # reduce update_delay to speed up simulation
    sim.run(n_trials=10)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
