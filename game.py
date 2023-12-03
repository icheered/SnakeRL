import numpy as np

class Game:
    def __init__(self, w=20, h=20):
        self.width = w
        self.height = h

        self.board = np.zeros((self.width, self.height))
        self.snake = []
        self.score = 0

        self.frame = 0
        self.frames_without_food = 0

    def reset(self):
        self.frame = 0
        self.frames_without_food = 0
        self.score = 0
        self.board = np.zeros((self.width, self.height))
        
        mid_x = self.width // 2
        mid_y = self.height // 2
        self.snake = [(mid_y, mid_x - 1), (mid_y, mid_x), (mid_y, mid_x + 1)]

        # Place the snake on the board
        for segment in self.snake:
            self.board[segment] = 1

        # Mark the head of the snake (last segment) with a 2
        self.board[self.snake[-1]] = 2

        self._place_food()

    def _place_food(self):
        # Get all the empty cells
        empty_cells = np.argwhere(self.board == 0)

        # Pick one at random
        food = empty_cells[np.random.choice(empty_cells.shape[0])]

        # Place the food
        self.board[food[0], food[1]] = 10

    def _move(self, action) -> (int, bool):
        # Action: 0 -> up, 1 -> right, 2 -> down, 3 -> left
        head = self.snake[-1]
        new_head = None

        if action == 0:
            # Up
            new_head = (head[0] - 1, head[1])
        elif action == 1:
            # Right
            new_head = (head[0], head[1] + 1)
        elif action == 2:
            # Down
            new_head = (head[0] + 1, head[1])
        elif action == 3:
            # Left
            new_head = (head[0], head[1] - 1)

        # Check if the snake hit a wall
        if new_head[0] < 0 or new_head[0] >= self.height or new_head[1] < 0 or new_head[1] >= self.width:
            # Snake hit a wall
            return -1, True

        # Check if the snake hit itself
        if new_head in self.snake:
            # Snake hit itself
            return -1, True

        # Check if the snake ate food
        ate_food = False
        if self.board[new_head] == 10:
            # Snake ate food
            ate_food = True
            self.frames_without_food = 0
            self._place_food()
        else:
            # Remove the tail
            self.frames_without_food += 1
            self.board[self.snake[0]] = 0
            self.snake.pop(0)
        
        if(self.frames_without_food > 400):
            print("Snake starved to death")
            return 0, True

        # Add the new head
        self.board[self.snake[-1]] = 1
        self.snake.append(new_head)
        self.board[new_head] = 1

        # Mark the head of the snake (last segment) with a 2
        self.board[self.snake[-1]] = 2

        return int(ate_food), False
    
    def get_direction(self):
        # Find the current direction based on the head and the previous segment
        head = self.snake[-1]
        previous_segment = self.snake[-2]
        direction = (head[0] - previous_segment[0], head[1] - previous_segment[1])
        
        # Find the direction
        if direction == (0, 1):
            return 1
        elif direction == (0, -1):
            return 3
        elif direction == (1, 0):
            return 2
        elif direction == (-1, 0):
            return 0
    
    def moving_to_apple(self):
        # Check the head and second segment
        # If the head is closer to the apple, return 1
        # If the second segment is closer to the apple, return -1
        # Otherwise, return 0
        head = self.snake[-1]
        second_segment = self.snake[-2]
        apple = np.argwhere(self.board == 10)[0]

        head_distance = abs(head[0] - apple[0]) + abs(head[1] - apple[1])
        second_segment_distance = abs(second_segment[0] - apple[0]) + abs(second_segment[1] - apple[1])

        if head_distance < second_segment_distance:
            return 2
        elif head_distance > second_segment_distance:
            return -1
        else:
            return 0
    
    def distance_to_apple(self):
        head = self.snake[-1]
        apple = np.argwhere(self.board == 10)[0]

        return abs(head[0] - apple[0]) + abs(head[1] - apple[1])

    def print_board(self):
        print(" " + "_" * (self.width))
        for row in self.board:
            print("|", end="")
            for cell in row:
                if cell == 0:
                    print(" ", end="")
                elif cell == 1:
                    print("o", end="")
                elif cell == 2:
                    print("H", end="")
                elif cell == 10:
                    print("*", end="")
            print("|", end="")
            print()
        print(" " + "_" * (self.width))

    def get_state(self):
        return self.board
    
    def step(self, action):
        # Action: 0 -> up, 1 -> right, 2 -> down, 3 -> left
        self.frame += 1

        # Move the snake
        ate_food, done = self._move(action)

        # Update score        
        if ate_food:
            self.score += 1
        
        #print(f"Frame: {self.frame}, Score: {self.score}, Frames without food: {self.frames_without_food}")
        
        return self.score, done