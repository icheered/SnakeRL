import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet, QTrainer
import time

MAX_MEMORY = 100_000
BATCH_SIZE = 100
LR = 0.01  # learning rate

class Agent:
    def __init__(self, game):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.99 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(game.width * game.height + 4, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        pass

    def get_action(self, game):
        # Flatten board
        state = game.get_state()

        # random moves: tradeoff exploration / exploitation
        self.epsilon = 150 - (self.n_games/25)
        move = 0
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
        
        #0 = up, 1 = right, 2 = down, 3= left
        return move

    def get_reward(self, score, old_score, done, game):
        if(done):
            return -100, 0, 0
        score_reward = (score - old_score) * 10
        distance_to_apple = 20-game.distance_to_apple()
        moving_to_apple = game.moving_to_apple()*0.2 
        survive_duration_reward = game.frame * 0.5

        return round(score_reward), round(distance_to_apple,1), round(survive_duration_reward,2)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def load(self):
        pass
