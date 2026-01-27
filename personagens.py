import pygame

class Personagens():
    def __init__(self, x, y, jogador, sprite_sheet, vida):
        self.jogador = jogador
        self.sprite_sheet = sprite_sheet
        self.vida_maxima = vida
        self.vida = vida
        # Guardar posição inicial para o reset
        self.pos_inicial_x = x
        self.pos_inicial_y = y

        self.frame_largura = 80
        self.frame_altura = 180

        self.action = "parado"
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.flip = False

        self.vel_y = 0
        self.pulando = False
        self.atacando = False
        self.vivo = True
        self.tempo_cooldown = 600
        self.ultimo_ataque = 0

        self.rect = pygame.Rect(x, y, 80, 180)
        self.animacoes = self.carregar_animacoes()
        self.image = self.animacoes[self.action][self.frame_index]

    def carregar_animacoes(self):
        anim = {}
        def pegar_frames(linha, inicio, fim):
            frames = []
            for i in range(inicio, fim + 1):
                frame = self.sprite_sheet.subsurface(
                    i * self.frame_largura,
                    linha * self.frame_altura,
                    self.frame_largura,
                    self.frame_altura
                )
                frames.append(frame)
            return frames

        if self.jogador == 1:
            anim["parado"]  = pegar_frames(2, 0, 2)
            anim["andando"] = pegar_frames(0, 0, 3)
            anim["pulando"] = pegar_frames(0, 5, 10)
            anim["soco"]    = pegar_frames(1, 5, 7)
            anim["chute"]   = pegar_frames(1, 0, 4)
            anim["morte"]   = pegar_frames(0, 4, 4)
        else:
            anim["parado"]  = pegar_frames(0, 4, 6)
            anim["andando"] = pegar_frames(0, 0, 3)
            anim["pulando"] = pegar_frames(2, 0, 5)
            anim["soco"]    = pegar_frames(0, 7, 9)
            anim["chute"]   = pegar_frames(1, 0, 4)
            anim["morte"]   = pegar_frames(1, 5, 5)
        return anim

    def move(self, largura, altura, alvo, round_fim):
        if round_fim or not self.vivo:
            return

        velocidade = 6
        dx = 0
        dy = 0
        teclas = pygame.key.get_pressed()
        movendo = False

        # Só permite comandos se não estiver atacando
        if not self.atacando:
            if self.jogador == 1:
                if teclas[pygame.K_a]:
                    dx = -velocidade
                    movendo = True
                elif teclas[pygame.K_d]:
                    dx = velocidade
                    movendo = True
                if teclas[pygame.K_w] and not self.pulando:
                    self.vel_y = -18
                    self.pulando = True
                if teclas[pygame.K_c]:
                    self.atacar("soco", alvo)
                elif teclas[pygame.K_v]:
                    self.atacar("chute", alvo)
            else:
                if teclas[pygame.K_LEFT]:
                    dx = -velocidade
                    movendo = True
                elif teclas[pygame.K_RIGHT]:
                    dx = velocidade
                    movendo = True
                if teclas[pygame.K_UP] and not self.pulando:
                    self.vel_y = -18
                    self.pulando = True
                if teclas[pygame.K_o]:
                    self.atacar("soco", alvo)
                elif teclas[pygame.K_p]:
                    self.atacar("chute", alvo)

        # Gerenciamento de Animações (Prioridade para o ataque)
        if self.atacando:
            pass # Deixa a animação de soco/chute rodar até o fim
        elif self.pulando:
            self.set_action("pulando")
        elif movendo:
            self.set_action("andando")
        else:
            self.set_action("parado")

        # Gravidade
        self.vel_y += 1
        dy += self.vel_y

        # Colisão com o chão
        chao = 395
        if self.rect.bottom + dy > chao:
            dy = chao - self.rect.bottom
            self.vel_y = 0
            self.pulando = False

        self.rect.x += dx
        self.rect.y += dy

        # Limites da tela
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > largura: self.rect.right = largura

        # Girar personagem para o alvo
        distancia = self.rect.centerx - alvo.rect.centerx
        if self.jogador == 1:
            self.flip = distancia > 0
        else:
            self.flip = distancia < 0

    def atacar(self, tipo, alvo):
        tempo_atual = pygame.time.get_ticks()
        if self.atacando or (tempo_atual - self.ultimo_ataque < self.tempo_cooldown):
            return

        self.atacando = True
        self.ultimo_ataque = tempo_atual
        self.set_action(tipo)

        # Hitboxes diferenciadas
        if tipo == "chute":
            largura_hitbox = 60
            altura_hitbox = 40
            offset_y = 100
        else: # soco
            largura_hitbox = 30
            altura_hitbox = 80
            offset_y = 50

        olhando_para_direita = (not self.flip) if self.jogador == 1 else self.flip

        if olhando_para_direita:
            hitbox_x = self.rect.right
        else:
            hitbox_x = self.rect.left - largura_hitbox

        hitbox = pygame.Rect(hitbox_x, self.rect.y + offset_y, largura_hitbox, altura_hitbox)

        if hitbox.colliderect(alvo.rect):
            if tipo == "soco":
                alvo.vida -= 9
            elif tipo == "chute":
                alvo.vida -= 15
            
            if alvo.vida <= 0:
                alvo.vida = 0
                alvo.vivo = False
                alvo.set_action("morte")

    def set_action(self, nova):
        if self.action != nova:
            self.action = nova
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def atualizar_animacao(self):
        tempo_frame = 120 
        
        # Proteção de índice caso a lista de frames mude
        if self.frame_index >= len(self.animacoes[self.action]):
            self.frame_index = 0

        self.image = self.animacoes[self.action][self.frame_index]
        
        if pygame.time.get_ticks() - self.update_time > tempo_frame:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            
            if self.frame_index >= len(self.animacoes[self.action]):
                if not self.vivo:
                    self.frame_index = len(self.animacoes[self.action]) - 1 
                else:
                    # Se terminou um ataque, volta a permitir movimento/outras animações
                    if self.action == "soco" or self.action == "chute":
                        self.atacando = False
                    self.frame_index = 0

    def reset(self, x, y):
        self.vida = self.vida_maxima
        self.vivo = True
        self.atacando = False
        self.pulando = False
        self.vel_y = 0
        self.rect.x = x
        self.rect.y = y
        self.set_action("parado")

    def desenho(self, screen):
        self.atualizar_animacao()
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, self.rect)