import pygame

def get_human_action(action):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                action = 0
            if event.key == pygame.K_RIGHT:
                action = 1
            elif event.key == pygame.K_DOWN:
                action = 2
            elif event.key == pygame.K_LEFT:
                action = 3
                
    return action
                
