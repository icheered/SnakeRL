import pygame

class Human:
    def __init__(self):
        pass

    def get_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Get left and right arrow keys
        keys = pygame.key.get_pressed()
        action = 0
        if keys[pygame.K_LEFT]:
            action = 0
        elif keys[pygame.K_RIGHT]:
            action = 2
        else:
            action = 1

        return action