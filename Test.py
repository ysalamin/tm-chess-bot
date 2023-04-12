import pygame

pygame.init()

WIDTH, HEIGHT = 1280, 1280
screen = pygame.display.set_mode((WIDTH, HEIGHT))
while True:
    for event in pygame.event.get():
        if event.type == pygame.quit:
            pygame.quit()