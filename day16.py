import math
import random

import numpy as np
import torch
from torch import nn, relu
from torch.autograd.grad_mode import F
from torch.nn import MSELoss
from torch.nn.modules import Module, Linear, Conv2d
from torch.optim import Adam

BATCH_SIZE = 32
EPSILON = 0.9
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.99
GAMMA = 0.99
LEARNING_RATE = 0.001
MEMORY_MAX = 1000

class Agent(Module):

    def __init__(self, state_space, action_space, **kwargs):
        super(Agent, self).__init__()

        self.state_space = state_space
        self.action_space = action_space

        self.epsilon = EPSILON
        self.epsilon_min = EPSILON_MIN
        self.epsilon_decay = EPSILON_DECAY
        self.gamma = GAMMA
        self.learning_rate = LEARNING_RATE

        self.in_layer = Linear(state_space, 128)
        self.hidden_layer = Linear(128, 64)
        self.out_layer = Linear(64, action_space)

        self.loss_fn = MSELoss()
        self.optimizer = Adam(self.parameters(), lr=self.learning_rate)

    def forward(self, state):
        x = relu(self.in_layer(state))
        x = relu(self.hidden_layer(x))
        policy = self.out_layer(x)
        return policy

    def act(self, state):
        if torch.rand(1) > self.epsilon:
            action = self(state).max(0)[1].view(1, 1)
        else:
            action = torch.tensor([[random.randrange(self.action_space)]])
        self.reduce_epsilon()
        return action

    def learn(self, state, action, reward, next_state, done):
        q_current = self(state)[action]

        if done:
            q_target = torch.tensor(reward)
        else:
            q_next = torch.max(self(next_state))
            q_target = torch.tensor(reward + (self.gamma * q_next))

        q_target = q_target.unsqueeze(1)
        q_target.requires_grad_()

        loss = self.loss_fn(q_current, q_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def reduce_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay



def get_actions(valves, current_valve):
    actions = []
    for connection in current_valve.connections:
        actions.append(valves[connection].action_nb)
    if current_valve.open:
        actions.append(0)


def step(action_space, current_valve, action):
    if action == 0:
        return current_valve, current_valve.flow_rate
    return action_space[action], 0


def run_simulation(agent, valves, action_space, starting_valve, time):

    current_valve = starting_valve
    while time > 0:
        action = agent.act(current_valve)
        next_state, reward, done, _ = step(action_space, current_valve. action)

        reward = torch.tensor([reward], dtype=torch.float32)
        if done:
            next_state = None
        else:
            next_state = torch.tensor(next_state, dtype=torch.float32)

        agent.learn(state, action, reward, next_state, done)

        state = next_state

        time -= 1


class Valve:

    def __init__(self, name, flow_rate, connections, action_nb):
        self.name = name
        self.flow_rate = flow_rate
        self.connections = connections
        self.action_nb = action_nb
        self.open = False

    def __call__(self, *args, **kwargs):
        return [self.action_nb, int(self.open)]


with open("resources/day16.txt", 'r') as f:
    lines = f.read().splitlines()
    valves = {}
    action_nb = 1
    for line in lines:
        line_parts = line.split(" ")
        name = line_parts[1]
        flow_rate = line_parts[4][5:-1]
        connections = [i.replace(',', '') for i in line_parts[9:]]

        valves[name] = Valve(name, int(flow_rate), connections, action_nb)
        action_nb += 1

    state_space = torch.tensor([2])
    action_space = [i for i in range(action_nb)]
    agent = Agent(state_space, action_space)
    run_simulation(agent, valves, action_space, valves['AA'], 30)
