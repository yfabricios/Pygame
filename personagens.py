import pygame

class Personagens():
    def __init__(self, jogador, x, y, virar, data, sprite_sheet, passos_animacao):
        self.jogador = jogador
        self.tamanho = data[0]
        self.escala_imagem = data[1]
        self.offset = data[2]
        self.virar = virar
        self.lista_animacao = self.carregar_imagens(sprite_sheet, passos_animacao)
        self.action = 0 #0: parado, 1:correndo , 2:pulando, 3: soco, 4:chute, 5: acertado, 6: morto
        self.frame_index = 0
        self.imagem = self.lista_animacao[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.corrrendo = False
        self.pulo = False
        self.atacando = False
        self.tipo_de_ataque = 0
        self.ataque_cooldown = 0
        self.golpeado = False
        self.vida = 100
        self.vivo = True

    def carregar_imagens(self, sprite_sheet, passos_animacao):
        #extrair imagens do spritesheet
        lista_animacao = []
        for y, animacao in enumerate(passos_animacao):
            lista_img_temp = []
            for x in range(animacao):
                img_temp = sprite_sheet.subsurface(x, y, 80, 180)
                lista_img_temp.append(pygame.transform.scale(img_temp, (self.tamanho * self.escala_imagem, self.tamanho * self.escala_imagem)))
            lista_animacao.append(lista_img_temp)
        return lista_animacao

    def move(self, tela_largura, tela_altura, superface, alvo):
        velocidade = 8
        gravidade = 2
        dx = 0
        dy = 0
        self.corrrendo = False
        self.tipo_de_ataque = 0

# Precionamento das teclas
        key = pygame.key.get_pressed()

#só pode fazer outras ações se não estiver atacando
        if self.atacando == False and self.vivo == True:

    #checando os controles do jogador 1
            if self.jogador == 1:

    # Movimento
                if key[pygame.K_a]:
                    dx = -velocidade
                    self.corrrendo = True
                if key[pygame.K_d]:
                    dx = velocidade
                    self.corrrendo = True
        #pulo   
                if key[pygame.K_w] and self.pulo == False:
                    self.vel_y = -30
                    self.pulo = True
        #ataques
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.ataque(superface, alvo)

                    #determinar o tipo de ataque que será usado
                    if key[pygame.K_r]:
                        self.tipo_de_ataque = 1
                    if key[pygame.K_t]:
                        self.tipo_de_ataque = 2
#checando os controles do jogador 2
            if self.jogador == 2 and self.vivo == True:
    # Movimento
                if key[pygame.K_LEFT]:
                    dx = -velocidade
                    self.corrrendo = True
                if key[pygame.K_RIGHT]:
                    dx = velocidade
                    self.corrrendo = True
        #pulo   
                if key[pygame.K_UP] and self.pulo == False:
                    self.vel_y = -30
                    self.pulo = True
        #ataques
                if key[pygame.K_o] or key[pygame.K_p]:
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
        if self.rect.bottom + dy > (tela_altura - 160):
            self.vel_y = 0
            self.pulo = False
            dy = (tela_altura - 160) - self.rect.bottom

# garantir que o jogador ataque na direção que o alvo se encontra
        if alvo.rect.centerx > self.rect.centerx:
            self.virar = False
        if alvo.rect.centerx < self.rect.centerx:
            self.virar = True

#aplicar cooldown de ataque
        if self.ataque_cooldown > 0:
            self.ataque_cooldown -= 1
# uptade da posição do player
        self.rect.x += dx
        self.rect.y += dy

#atualizar as animações
    def atualizar(self):
        #checar qual a ação que o player está fazendo
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False
            self.update_action(6)
        elif self.golpeado == True:
            self.update_action(5)
        elif self.atacando == True:
            if self.tipo_de_ataque == 1:
                self.update_action(3)
            elif self.tipo_de_ataque == 2:
                self.update_action(4)
        elif self.pulo == True:
            self.update_action(2)
        elif self.corrrendo == True:
            self.update_action(1)
        else:
            self.update_action(0)
        cooldown_animacao = 5
        #atualizar imagem
        self.imagem = self.lista_animacao[self.action][self.frame_index]
        #checar se passou tempo suficiente desde a ultima atualização
        if pygame.time.get_ticks() - self.update_time > cooldown_animacao:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #checar se a animação foi finalizada
        if self.frame_index >= len(self.lista_animacao[self.action]):
            #se o player esta morto a animação para
            if self.vivo == False:
                self.frame_index = len(self.lista_animacao[self.action]) - 1
            else:
                self.frame_index = 0
                #checar se um ataque foi executado
                if self.action == 3 or self.action == 4:
                    self.atacando = False
                    self.ataque_cooldown = 20
                #checar se o dano foi recebido
                if self.action == 5:
                    self.golpeado = False
                    #se o jogador estiver no meio do ataque, o ataque será parado
                    self.atacando = False
                    self.ataque_cooldown = 20

    def ataque(self, superface, alvo,):
        if self.ataque_cooldown == 0:
            self.atacando = True
            retangulo_de_ataque = pygame.Rect(self.rect.centerx - (2 * self.rect.width), self.rect.y, 2*self.rect.width, self.rect.height)
            if retangulo_de_ataque.colliderect(alvo.rect):
                alvo.vida -= 10
                alvo.golpeado = True
            pygame.draw.rect(superface, (0, 255, 0), retangulo_de_ataque)

    def update_action(self, new_action):
        #checar se a nova ação é diferente da anterior
        if new_action != self.action:
            self.action = new_action
            #atualizar configurações de animação  
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def desenho(self, superface):
        img = pygame.transform.flip(self.imagem, self.virar, False)
        pygame.draw.rect(superface, (255, 0, 0), self.rect)
        superface.blit(self.imagem, (self.rect.x - (self.offset[0] * self.escala_imagem), self.rect.y - (self.offset[1] * self.escala_imagem)))