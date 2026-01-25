import pygame
import os

class Personagens():
    def __init__(self, player, x, y):
        self.player = player
        self.flip = False
        self.vivo = True
        self.vida = 100

        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.animation_list = self.carregar_animacoes()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def carregar_animacoes(self):
        animation_list = []

        base_path = os.path.dirname(__file__)
        sheet_path = os.path.join(base_path, "Plazer1.png")

        if not os.path.exists(sheet_path):
            raise FileNotFoundError(f"Sprite não encontrada em: {sheet_path}")

        sheet = pygame.image.load(sheet_path).convert_alpha()

        SPRITE_LARGURA = 80
        SPRITE_ALTURA = 180

        animacoes = [4, 4, 6, 5, 5, 1]

        for linha, frames in enumerate(animacoes):
            temp_list = []
            for coluna in range(frames):
                frame = sheet.subsurface(
                    coluna * SPRITE_LARGURA,
                    linha * SPRITE_ALTURA,
                    SPRITE_LARGURA,
                    SPRITE_ALTURA
                )
                temp_list.append(frame)
            animation_list.append(temp_list)

        return animation_list


    def move(self, largura_tela, altura_tela, surface, alvo, round_fim):
        velocidade = 5
        dx = 0

        teclas = pygame.key.get_pressed()

        if not round_fim and self.vivo:
            if self.player == 1:
                if teclas[pygame.K_a]:
                    dx = -velocidade
                    self.flip = True
                if teclas[pygame.K_d]:
                    dx = velocidade
                    self.flip = False
            else:
                if teclas[pygame.K_LEFT]:
                    dx = -velocidade
                    self.flip = True
                if teclas[pygame.K_RIGHT]:
                    dx = velocidade
                    self.flip = False

        self.rect.x += dx
        self.atualizar_animacao()

    def atualizar_animacao(self):
        ANIMATION_COOLDOWN = 100

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def desenho(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, self.rect)