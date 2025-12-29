import pygame

class Personagens():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False

    def move(self):
        velociade = 10
        gravidade = 2
        dx = 0
        dy = 0

# Precionamento das teclas
        key = pygame.key.get_pressed()

# Movimento
        if key[pygame.K_a]:
            dx = -velociade
        if key[pygame.K_d]:
            dx = velociade
#pulo
        if key[pygame.K_w] and self.jump == False:
            self.vel_y = -30
            self.jump = True
#aplicar gravidade
        self.vel_y += gravidade
        dy += self.vel_y

#garantir que o player não saia da tela
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > 1000:
            dx = 1000 - self.rect.right
        if self.rect.bottom + dy > 453:
            self.vel_y = 0
            self.jump = False
            dy = 463 - self.rect.bottom

# uptade da posição do player
        self.rect.x += dx
        self.rect.y += dy

    def desenho(self, superface):
        pygame.draw.rect(superface, (255, 0, 0), self.rect)