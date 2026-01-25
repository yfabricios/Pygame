import pygame
import os

class Personagens(pygame.sprite.Sprite):
    def __init__(self, jogador, x, y):
        super().__init__()

        self.jogador = jogador
        self.virar = False
        self.rect = pygame.Rect(x, y, 80, 180)

        # estado físico
        self.vel_y = 0
        self.pulo = False

        # combate
        self.atacando = False
        self.tipo_de_ataque = 0
        self.tempo_ataque = 0
        self.cooldown_ataque = 0

        # vida
        self.vida = 100
        self.vivo = True

        # animação
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # carregar animações
        self.animation_list = self.carregar_animacoes()

        self.image = self.animation_list[self.action][self.frame_index]

    # --------------------------------------------------
    
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

    # --------------------------------------------------
    def update_animation(self):
        ANIMATION_COOLDOWN = 100

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 5:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.action = 0
                    self.frame_index = 0

        self.image = self.animation_list[self.action][self.frame_index]

    # --------------------------------------------------
    def move(self, tela_largura, tela_altura, superficie, alvo, round_fim):
        velocidade = 10
        gravidade = 2
        dx = dy = 0

        key = pygame.key.get_pressed()

        if self.vivo and not round_fim and not self.atacando:

            if self.jogador == 1:
                if key[pygame.K_a]:
                    dx = -velocidade
                    self.action = 1
                if key[pygame.K_d]:
                    dx = velocidade
                    self.action = 1
                if key[pygame.K_w] and not self.pulo:
                    self.vel_y = -25
                    self.pulo = True
                    self.action = 2
                if key[pygame.K_r] and self.cooldown_ataque == 0:
                    self.atacar(superficie, alvo, 3)
                if key[pygame.K_t] and self.cooldown_ataque == 0:
                    self.atacar(superficie, alvo, 4)

            if self.jogador == 2:
                if key[pygame.K_LEFT]:
                    dx = -velocidade
                    self.action = 1
                if key[pygame.K_RIGHT]:
                    dx = velocidade
                    self.action = 1
                if key[pygame.K_UP] and not self.pulo:
                    self.vel_y = -25
                    self.pulo = True
                    self.action = 2
                if key[pygame.K_o] and self.cooldown_ataque == 0:
                    self.atacar(superficie, alvo, 3)
                if key[pygame.K_p] and self.cooldown_ataque == 0:
                    self.atacar(superficie, alvo, 4)

        self.vel_y += gravidade
        dy += self.vel_y

        if self.rect.bottom + dy > tela_altura - 205:
            dy = tela_altura - 205 - self.rect.bottom
            self.vel_y = 0
            self.pulo = False

        if self.vida <= 0:
            self.vivo = False
            self.action = 5

        self.rect.x += dx
        self.rect.y += dy

    # --------------------------------------------------
    def atacar(self, superficie, alvo, tipo):
        self.atacando = True
        self.cooldown_ataque = 30
        self.action = tipo
        self.frame_index = 0

        ataque_rect = pygame.Rect(
            self.rect.centerx - (2 * self.rect.width * self.virar),
            self.rect.y,
            2 * self.rect.width,
            self.rect.height
        )

        if ataque_rect.colliderect(alvo.rect):
            alvo.vida -= 10

    # --------------------------------------------------
    def desenho(self, superficie):
        self.update_animation()

        img = pygame.transform.flip(self.image, self.virar, False)
        superficie.blit(img, self.rect)