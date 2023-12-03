import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001  # learning rate

class Agent:
    def __init__(self, game):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(game.width * game.height, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        pass

    def get_action(self, game, previous_move):
        # Flatten board
        state = np.array(game.get_state(), dtype=np.float32).flatten()
        invalid_move = game.get_invalid_move()

        # random moves: tradeoff exploration / exploitation
        self.epsilon = 100 - min(self.n_games/10, 80)
        move = previous_move
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
        
        #print(f"Previous: {previous_move}, Current: {move}")
        if move == invalid_move:
            move = previous_move

        return move

    def get_reward(self, score, old_score, done, game):
        if(done):
            return -20
        score_reward = (score - old_score) * 30
        moving_to_apple = game.moving_to_apple()
        survive_duration_reward = game.frame * 0.2

        return score_reward + moving_to_apple + survive_duration_reward

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        
    def train_short_memory(self, state, action, reward, next_state, done):
        state = np.array(state, dtype=np.float32).flatten()
        next_state = np.array(next_state, dtype=np.float32).flatten()
        self.trainer.train_step(state, action, reward, next_state, done)


    def remember(self, state, action, reward, next_state, done):
        state = np.array(state, dtype=np.float32).flatten()
        next_state = np.array(next_state, dtype=np.float32).flatten()
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def load(self):
        pass