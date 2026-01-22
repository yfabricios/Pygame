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

    #spritesheets
    # plazer1_sheets = pygame.image.load("Plazer1.png").convert_alpha()
    # reihard2_sheets = pygame.image.load("Reihard2.png").convert_alpha()

    # #passos de cada animação

    # #plazer
    # plazer_andando = []
    # for i in range (0, 4):
    #     img = plazer1_sheets.subsurface(i*80, 0), (80, 180)
    #     plazer_andando.append(img)

    # plazer_morre = []
    # for i in range (4, 5):
    #     img = plazer1_sheets.subsurface(i*80, 0), (80, 180)
    #     plazer_morre.append(img)

    # plazer_pulando = []
    # for i in range (5, 11):
    #     img = plazer1_sheets.subsurface(i*80, 0), (80, 180)
    #     plazer_pulando.append(img)
    
    # plazer_chutando = []
    # for i in range (0, 5):
    #     img = plazer1_sheets.subsurface(i*80, 180), (80, 180)
    #     plazer_chutando.append(img)

    # plazer_socando = []
    # for i in range (5, 8):
    #     img = plazer1_sheets.subsurface(i*80, 180), (80, 180)
    #     plazer_socando.append(img)

    # plazer_parado = []
    # for i in range (0, 3):
    #     img = plazer1_sheets.subsurface(i*80, 360), (80, 180)
    #     plazer_parado.append(img)

    # #reihard

    # reihard_andando = []
    # for i in range (0, 4):
    #     img = reihard2_sheets.subsurface(i*80, 0), (80, 180)
    #     reihard_andando.append(img)

    # reihard_morre = []
    # for i in range (5, 6):
    #     img = reihard2_sheets.subsurface(i*80, 180), (80, 180)
    #     reihard_morre.append(img)

    # reihard_pulando = []
    # for i in range (0, 6):
    #     img = reihard2_sheets.subsurface(i*80, 360) (80, 180)
    #     reihard_pulando.append(img)
    
    # reihard_chutando = []
    # for i in range (0, 5):
    #     img = reihard2_sheets.subsurface(i*80, 180), (80, 180)
    #     reihard_chutando.append(img)

    # reihard_socando = []
    # for i in range (7, 10):
    #     img = reihard2_sheets.subsurface(i*80, 0), (80, 180)
    #     reihard_socando.append(img)

    # reihard_parado = []
    # for i in range (4, 7):
    #     img = reihard2_sheets.subsurface(i*80, 0), (80, 180)
    #     reihard_parado.append(img)

    # #pacote de animação
    # plazer_pacote = [plazer_parado, plazer_andando, plazer_pulando, plazer_socando, plazer_chutando, plazer_morre]
    # reihard_pacote = [reihard_parado, reihard_andando, reihard_pulando, reihard_socando, reihard_chutando, reihard_morre]
    # pacote_anima = [plazer_parado, plazer_andando, plazer_pulando, plazer_socando, plazer_chutando, plazer_morre, reihard_parado, reihard_andando, reihard_pulando, reihard_socando, reihard_chutando, reihard_morre]
    
    # def action(pacote_anima, plazer_action, reihard_action):
    #     if plazer_action == 0:
    #         for i in range (len(pacote_anima[plazer_action])):
    #             img_temp = pacote_anima[plazer_action][i]
    #     if plazer_action == 1:
    #         for i in range (len(pacote_anima[plazer_action])):
    #             img_temp = pacote_anima[plazer_action][i]   
    #     if plazer_action == 2:
    #         for i in range (len(pacote_anima[plazer_action])):
    #             img_temp = pacote_anima[plazer_action][i]
    #     if plazer_action == 3:
    #         for i in range (len(pacote_anima[plazer_action])):
    #             img_temp = pacote_anima[plazer_action][i]
    #     if plazer_action == 4:
    #         for i in range (len(pacote_anima[plazer_action])):
    #             img_temp = pacote_anima[plazer_action][i]
    #     if plazer_action == 5:
    #         for i in range (len(pacote_anima[plazer_action])):
    #             img_temp = pacote_anima[plazer_action][i] 
    #     if reihard_action == 6:
    #         for i in range (len(pacote_anima[reihard_action])):
    #             img_temp = pacote_anima[reihard_action][i]
    #     if reihard_action == 7:
    #         for i in range (len(pacote_anima[reihard_action])):
    #             img_temp = pacote_anima[reihard_action][i]
    #     if reihard_action == 8:
    #         for i in range (len(pacote_anima[reihard_action])):
    #             img_temp = pacote_anima[reihard_action][i]
    #     if reihard_action == 9:
    #         for i in range (len(pacote_anima[reihard_action])):
    #             img_temp = pacote_anima[reihard_action][i]
    #     if reihard_action == 10:
    #         for i in range (len(pacote_anima[reihard_action])):
    #             img_temp = pacote_anima[reihard_action][i]
    #     if reihard_action == 11:
    #         for i in range (len(pacote_anima[reihard_action])):
    #             img_temp = pacote_anima[reihard_action][i]
