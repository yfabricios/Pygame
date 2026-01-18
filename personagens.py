import pygame

class Personagens():
    def __init__(self, x, y, virar, data, sprite_sheet, passos_animacao):
        self.tamanho = data[0]
        self.escala_imagem = data[1]
        self.offset = data[2,]
        self.virar = virar
        self.lista_animacao = self.carregar_imagens(sprite_sheet, passos_animacao)
        self.action = 0 #0: parado, 1:correndo , 2:pulando, 3: soco, 4:chute, 5: acertado, 6: morto
        self.frame_index = 0
        self.imagem = self.lista_animacao[self.action][self.frame_index]
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.pulo = False
        self.atacando = False
        self.tipo_de_ataque = 0
        self.vida = 100

    def carregar_imagens(self, sprite_sheet, passos_animacao):
        #extrair imagens do spritesheet
        lista_animacao = []
        for y, animacao in enumerate(passos_animacao):
            lista_img_temp = []
            for x in range(animacao):
                img_temp = sprite_sheet.subsurface(x*80, y*180, 80, 180)
                lista_img_temp.append(pygame.transform.scale(img_temp, (self.tamanho * self.escala_imagem, self.tamanho * self.escala_imagem)))
            lista_animacao.append(lista_img_temp)
        return lista_animacao

    def move(self, tela_largura, tela_altura, superface, alvo):
        velocidade = 10
        gravidade = 2
        dx = 0
        dy = 0

# Precionamento das teclas
        key = pygame.key.get_pressed()
#só pode fazer outras ações se não estiver atacando
        if self.atacando == False:
    # Movimento
            if key[pygame.K_a]:
                dx = -velocidade
            if key[pygame.K_d]:
                dx = velocidade
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

# uptade da posição do player
        self.rect.x += dx
        self.rect.y += dy

    def ataque(self, superface, alvo,):
        self.atacando = True
        retangulo_de_ataque = pygame.Rect(self.rect.centerx - (2 * self.rect.width), self.rect.y, 2*self.rect.width, self.rect.height)
        if retangulo_de_ataque.colliderect(alvo.rect):
            alvo.vida -= 10

        pygame.draw.rect(superface, (0, 255, 0), retangulo_de_ataque)

    def desenho(self, superface):
        img = pygame.transform.flip(self.iamgem, self.flip, False)
        pygame.draw.rect(superface, (255, 0, 0), self.rect)
        superface.blit(self.imagem, (self.rect.x - (self.offset[0] * self.escala_imagem), self.rect.y - (self.offset[1] * self.escala_imagem)))