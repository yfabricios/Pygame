import pygame

class Personagens():
    def __init__(self, jogador, x, y):
        self.jogador = jogador
        self.virar = False
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.pulo = False
        self.atacando = False
        self.tipo_de_ataque = 0
        self.tempo_ataque = 0
        self.vida = 100
        self.vivo = True
        self.tempo_ataque = 0
        self.cooldown_ataque = 0

    def move(self, tela_largura, tela_altura, superface, alvo, round_fim):
        velocidade = 10
        gravidade = 2
        dx = 0
        dy = 0

# tempo da trava de ataque
        if self.tempo_ataque > 0:
            self.tempo_ataque -= 1
        else:
            self.atacando = False

#cooldown
        if self.cooldown_ataque > 0:
            self.cooldown_ataque -= 1

# Precionamento das teclas
        key = pygame.key.get_pressed()

#só pode fazer outras ações se não estiver atacando
        if self.atacando == False and self.vivo == True and round_fim == False:
    # checar controles do jogador 1
            if self.jogador == 1:

        # Movimento
                if key[pygame.K_a]:
                    dx = -velocidade
                if key[pygame.K_d]:
                    dx = velocidade
            #pulo
                if key[pygame.K_w] and self.pulo == False:
                    self.vel_y = -25
                    self.pulo = True
            #ataques
                if (key[pygame.K_r] or key[pygame.K_t]) and self.cooldown_ataque == 0:
                    self.ataque(superface, alvo)
                #determinar o tipo de ataque que será usado
                    if key[pygame.K_r]:
                        self.tipo_de_ataque = 1
                    if key[pygame.K_t]:
                        self.tipo_de_ataque = 2
                        

    # checar controles do jogador 2
            if self.jogador == 2:

    # Movimento
                if key[pygame.K_LEFT]:
                    dx = -velocidade
                if key[pygame.K_RIGHT]:
                    dx = velocidade
        #pulo
                if key[pygame.K_UP] and self.pulo == False:
                    self.vel_y = -25
                    self.pulo = True
        #ataques
                if (key[pygame.K_o] or key[pygame.K_p]) and self.cooldown_ataque == 0:
                    self.ataque(superface, alvo)

                    #determinar o tipo de ataque que será usado
                    if key[pygame.K_o]:
                        self.tipo_de_ataque = 1
                    if key[pygame.K_p]:
                        self.tipo_de_ataque = 2
#aplicar gravidade
        self.vel_y += gravidade
        dy += self.vel_y

#garantir que o player não saia da tela
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > tela_largura:
            dx = tela_largura - self.rect.right
        if self.rect.bottom + dy > (tela_altura - 205):
            self.vel_y = 0
            self.pulo = False
            dy = (tela_altura - 205) - self.rect.bottom

# garantir que o jogador ataque na direção que o alvo se encontra
        if alvo.rect.centerx > self.rect.centerx:
            self.virar = False
        else:
            self.virar = True

# uptade da posição do player
        self.rect.x += dx
        self.rect.y += dy

    def ataque(self, superface, alvo,):
        self.atacando = True
        self.tempo_ataque = 15
        self.cooldown_ataque = 30

        retangulo_de_ataque = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.virar), self.rect.y, 2*self.rect.width, self.rect.height)
        if retangulo_de_ataque.colliderect(alvo.rect):
            alvo.vida -= 10

        pygame.draw.rect(superface, (0, 255, 0), retangulo_de_ataque)

    def desenho(self, superface):
        pygame.draw.rect(superface, (255, 0, 0), self.rect)
         