from gymnasium import Env
from gymnasium.spaces import Box, Discrete, MultiDiscrete
import numpy as np
import random
import math
from src.display import Display
import time

class SnakeEnv(Env):
    def __init__(self, config: dict, render_mode = None, max_episode_steps = 1000):
        self.width = config["game"]["width"]
        self.height = config["game"]["height"]
        
        # 0 = left, 1 = forward, 2 = right
        self.action_space = Discrete(3)
        self.observation_space = MultiDiscrete([4] * (self.width * self.height))

        # Reset to initialize the state 
        self.max_episode_steps = max_episode_steps
        self.episode_step = 0
        self.episodes_without_food = 0
        self.reset()
        
        # Initialize the display
        self.render_mode = render_mode
        if(self.render_mode == "human"):
            self.display = Display(
                config=config,
                title="Snake"
            )

    def get_state(self):
        return self.grid
    
    def seed(self, seed=None):
        # Set the seed
        random.seed(seed)
        # Return the seed
        return [seed]

    def reset(self, seed=None):
        # Reset the survive duration
        self.episode_step = 0
        self.episodes_without_food = 0

        # Create a grid of zeros
        self.grid = np.zeros((self.height, self.width), dtype=np.int32)

        # Pick a random place on the grid with a buffer of 3 squares from the edge
        mid_x = np.random.randint(3, self.width - 3)
        mid_y = np.random.randint(3, self.height - 3)

        # Pick a random direction (0: up, 1: right, 2: down, 3: left)
        direction = np.random.randint(0, 4)
        self.heading = (direction + 1) % 4

        # Initialize the snake based on the chosen direction
        if direction == 0:  # up
            self.snake = [(mid_y + 1, mid_x), (mid_y, mid_x), (mid_y - 1, mid_x)]
        elif direction == 1:  # right
            self.snake = [(mid_y, mid_x - 1), (mid_y, mid_x), (mid_y, mid_x + 1)]
        elif direction == 2:  # down
            self.snake = [(mid_y - 1, mid_x), (mid_y, mid_x), (mid_y + 1, mid_x)]
        else:  # left
            self.snake = [(mid_y, mid_x + 1), (mid_y, mid_x), (mid_y, mid_x - 1)]

        # Place the snake on the grid
        for segment in self.snake:
            self.grid[segment] = 1

        # Mark the head of the snake (last segment based on direction) with a 2
        self.grid[self.snake[-1]] = 2

        # Place the food
        self._place_food()

        # Convert the state to a numpy array with dtype float32
        obs = self.grid.flatten()

        info = {}
        return obs, info
    
    def _place_food(self):
        # Get all the empty cells
        empty_cells = np.argwhere(self.grid == 0)

        # Pick one at random
        food = empty_cells[np.random.choice(empty_cells.shape[0])]

        # Place the food
        self.grid[food[0], food[1]] = 3


    def render(self):
        mode = self.render_mode
        assert mode in ["human", None], "Invalid mode, must be either \"human\" or None"
        if mode == None:
            return
        elif mode == "human":
            self.display.update(self)
            time.sleep(0.1)


    def step(self, action):
        # Increment the survive duration
        self.episode_step += 1

        # Apply motor inputs
        self._apply_action(action)
        done, ate_apple = self._update_state_timestep()
        reward = self._get_reward(done, ate_apple)
        
        if self.episode_step > self.max_episode_steps:
            done = True
        
        # If snake has eaten 5 apples, end the episode
        if len(self.snake) > 8:
            done = True
            reward += 100

        info = {"episode_step": self.episode_step, "score": len(self.snake) - 3} if done else {}

        truncated = False

        # Convert state to numpy array with dtype float32, if not already done
        obs = self.grid.flatten()

        return obs, reward, done, truncated, info

    
    def _get_reward(self, done: bool, ate_apple: bool):
        # Calculate reward
        if done:
            return -100
        
        #direction_reward = self.moving_to_apple() * 0.2
        apple_reward = 100 if ate_apple else 0
        if apple_reward > 0:
            self.episodes_without_food = 0
        else:
            self.episodes_without_food += 1
        #starvation_punishment = -0.01 * max((self.episodes_without_food - 30),0)
        distance_to_apple_reward = -1 * (self._distance_to_apple() - 5)
        #if distance_to_apple_reward < 0:
            #distance_to_apple_reward /= 50
        length_reward = len(self.snake) - 3
        

        total_reward = apple_reward + distance_to_apple_reward + length_reward

        # print(f"Duration: {self.episodes_without_food}")
        # Print all rewards, rounded to 2 decimals
        #print(f"Direction reward: {direction_reward} | Apple reward: {apple_reward} | Starvation punishment: {starvation_punishment} | Distance to apple reward: {distance_to_apple_reward} | Length reward: {length_reward}")
        #print(f"Direction reward: {round(direction_reward,2)} | Apple reward: {round(apple_reward,2)} | Starvation punishment: {round(starvation_punishment,2)} | Distance to apple reward: {round(distance_to_apple_reward,2)} | Length reward: {round(length_reward,2)}")
        return total_reward

    def moving_to_apple(self):
        # Check the head and second segment
        # If the head is closer to the apple, return 1
        # If the second segment is closer to the apple, return -1
        # Otherwise, return 0
        head = self.snake[-1]
        second_segment = self.snake[-2]
        food = np.argwhere(self.grid == 3)[0]

        # Calculate the distance between the head and the food
        head_dist = math.sqrt((head[0] - food[0]) ** 2 + (head[1] - food[1]) ** 2)
        # Calculate the distance between the second segment and the food
        second_segment_dist = math.sqrt((second_segment[0] - food[0]) ** 2 + (second_segment[1] - food[1]) ** 2)

        if head_dist < second_segment_dist:
            return 0
        elif head_dist > second_segment_dist:
            return -1
        else:
            return 0
    
    def _distance_to_apple(self):
        # Check the head and second segment
        # If the head is closer to the apple, return 1
        # If the second segment is closer to the apple, return -1
        # Otherwise, return 0
        head = self.snake[-1]
        food = np.argwhere(self.grid == 3)[0]

        # Calculate the distance between the head and the food
        head_dist = math.sqrt((head[0] - food[0]) ** 2 + (head[1] - food[1]) ** 2)

        return head_dist


    def _apply_action(self, action):
        # 0 = left, 1 = forward, 2 = right
        # Change the heading of the snake
        if action == 0:
            self.heading = (self.heading - 1) % 4
        elif action == 2:
            self.heading = (self.heading + 1) % 4
        
    def _update_state_timestep(self):
        done = False
        ate_apple = False
        # Get the head of the snake
        head = self.snake[-1]

        # Get the new head of the snake
        if self.heading == 0:
            new_head = (head[0], head[1] - 1)
        elif self.heading == 1:
            new_head = (head[0] - 1, head[1])
        elif self.heading == 2:
            new_head = (head[0], head[1] + 1)
        elif self.heading == 3:
            new_head = (head[0] + 1, head[1])

        # Check if the snake has hit itself
        if new_head in self.snake:
            done = True
            return done, ate_apple
        
        # Check if the snake has hit a wall
        if new_head[0] < 0 or new_head[0] >= self.height or new_head[1] < 0 or new_head[1] >= self.width:
            done = True
            return done, ate_apple
        
        # Check if the snake has eaten the food
        if self.grid[new_head] == 3:
            # Place the food
            ate_apple = True
            self._place_food()
        else:
            # Check if snake has starved
            if self.episodes_without_food > 200:
                done = True
                return done, ate_apple
            # Remove the tail
            self.grid[self.snake[0]] = 0
            self.snake.pop(0)

        # Add the new head
        self.grid[self.snake[-1]] = 1
        self.snake.append(new_head)

        # Mark the head of the snake (last segment) with a 2
        self.grid[self.snake[-1]] = 2

        return done, ate_apple
  
    def close(self):
        # Call super class
        super().close()
        # Close the display
        if(self.render_mode == "human"):
            self.display.close()
