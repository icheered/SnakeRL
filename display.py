import pygame

pygame.init()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
font = pygame.font.Font("arial.ttf", 25)


class Display:
    def __init__(self, game, blocksize, title):
        self.grid = game.get_grid()
        self.blocksize = blocksize
        self.width = len(self.grid[0]) * blocksize
        self.height = len(self.grid) * blocksize

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

    def _draw_block(self, x, y, color):
        pygame.draw.rect(
            self.screen,
            color,
            [
                x * self.blocksize,
                y * self.blocksize,
                self.blocksize,
                self.blocksize,
            ],
        )

    def update(self, game):
        self.grid = game.get_grid()
        self.clock.tick(60)
        self.screen.fill(BLACK)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 1:
                    self._draw_block(j, i, WHITE)
                elif self.grid[i][j] == 2:
                    self._draw_block(j, i, GREEN)
                elif self.grid[i][j] == 10:
                    self._draw_block(j, i, RED)
        pygame.display.flip()
