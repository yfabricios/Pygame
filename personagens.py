import pygame

class Personagens():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))

    def move(self):
        velociade = 10
        dx = 0
        dy = 0

# Precionamento das teclas
        key = pygame.key.get_pressed()

# Movimento
        if key[pygame.K_a]:
            dx = -velociade
        if key[pygame.K_d]:
            dx = velociade

# uptade da posição do player
        self.rect.x += dx
        self.rect.y += dy

    def desenho(self, superface):
        pygame.draw.rect(superface, (255, 0, 0), self.rect)