import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0,255,0)
BLOCK_SIZE = 20   # Size of the motor squares

class Display:
    def __init__(self, config: dict, title: str):
        self.width = config["game"]["width"] * BLOCK_SIZE
        self.height = config["game"]["height"] * BLOCK_SIZE

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

    def _draw_block(self, x, y, color):
        pygame.draw.rect(
            self.screen,
            color,
            [
                x * BLOCK_SIZE,
                y * BLOCK_SIZE,
                BLOCK_SIZE,
                BLOCK_SIZE,
            ],
        )

    def update(self, game):
        self.grid = game.get_state()
        self.clock.tick(60)
        self.screen.fill(BLACK)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 1:
                    self._draw_block(j, i, WHITE)
                elif self.grid[i][j] == 2:
                    self._draw_block(j, i, GREEN)
                elif self.grid[i][j] == 3:
                    self._draw_block(j, i, RED)
        pygame.display.flip()

    def close(self):
        pygame.quit()