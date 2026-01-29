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
        
        # --- SISTEMA DE COOLDOWN E HIT ---
        self.tempo_cooldown = 1000  # 1 segundo de intervalo entre ataques
        self.ultimo_ataque = 0
        self.hit = False            # Indica se o personagem levou um golpe
        self.tempo_hit = 0          # Momento em que levou o golpe
        self.duracao_hit = 400      # Tempo (ms) que fica travado ao apanhar

        self.rect = pygame.Rect(x, y, 80, 180)
        self.animacoes = self.carregar_animacoes()
        self.image = self.animacoes[self.action][self.frame_index]

    def carregar_animacoes(self):
        anim = {}
        def pegar_frames(linha, inicio, fim, off_x=0, off_y=0):
            frames = []
            for i in range(inicio, fim + 1):
                pos_x = (i * self.frame_largura) + off_x
                pos_y = (linha * self.frame_altura) + off_y
                largura_recorte = self.frame_largura - off_x
                altura_recorte = self.frame_altura - off_y
                
                frame = self.sprite_sheet.subsurface(pos_x, pos_y, largura_recorte, altura_recorte)
                frames.append(frame)
            return frames

        if self.jogador == 1:
            anim["parado"]  = pegar_frames(2, 0, 2, off_y=10)
            anim["andando"] = pegar_frames(0, 0, 3)
            anim["pulando"] = pegar_frames(0, 5, 10)
            anim["soco"]    = pegar_frames(1, 5, 7, off_x=5, off_y=10)
            anim["chute"]   = pegar_frames(1, 0, 4, off_y=10)
            anim["morte"]   = pegar_frames(0, 4, 4)
        else:
            # Player 2
            anim["parado"]  = pegar_frames(0, 4, 6, off_x=10)
            anim["andando"] = pegar_frames(0, 0, 3)
            # Pulando, Chute e Morte agora com off_x=5
            anim["pulando"] = pegar_frames(2, 0, 5, off_x=5, off_y=10)
            anim["soco"]    = pegar_frames(0, 7, 9, off_x=5)
            anim["chute"]   = pegar_frames(1, 0, 4, off_x=3, off_y=10)
            anim["morte"]   = pegar_frames(1, 5, 5, off_x=5, off_y=5)
        return anim

    def move(self, largura, altura, alvo, round_fim):
        if round_fim or not self.vivo:
            return

        # Gerenciar recuperação do estado de Hit (atordoamento)
        tempo_atual = pygame.time.get_ticks()
        if self.hit:
            if tempo_atual - self.tempo_hit > self.duracao_hit:
                self.hit = False

        velocidade = 6
        dx = 0
        dy = 0
        teclas = pygame.key.get_pressed()
        movendo = False

        # Só permite comandos se NÃO estiver atacando E NÃO estiver atordoado (hit)
        if not self.atacando and not self.hit:
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

        # Gerenciamento de Animações
        if self.atacando:
            pass 
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

        # Aplicar movimento
        self.rect.x += dx
        self.rect.y += dy

        # Limites da tela
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > largura: self.rect.right = largura

        # Girar personagem para o alvo (apenas se não estiver morto)
        distancia = self.rect.centerx - alvo.rect.centerx
        if self.jogador == 1:
            self.flip = distancia > 0
        else:
            self.flip = distancia < 0

    def atacar(self, tipo, alvo):
        tempo_atual = pygame.time.get_ticks()
        # Impede ataque se estiver em cooldown ou se acabou de levar um golpe
        if self.atacando or (tempo_atual - self.ultimo_ataque < self.tempo_cooldown) or self.hit:
            return

        self.atacando = True
        self.ultimo_ataque = tempo_atual
        self.set_action(tipo)

        # Definição de Hitboxes e Força de Knockback
        if tipo == "chute":
            largura_hitbox = 45
            altura_hitbox = 30
            offset_y = 100
            forca_knockback = 30 # Empurrão forte
        else: # soco
            largura_hitbox = 30
            altura_hitbox = 80
            offset_y = 50
            forca_knockback = 20 # Empurrão leve

        olhando_para_direita = (not self.flip) if self.jogador == 1 else self.flip

        if olhando_para_direita:
            hitbox_x = self.rect.right
        else:
            hitbox_x = self.rect.left - largura_hitbox

        hitbox = pygame.Rect(hitbox_x, self.rect.y + offset_y, largura_hitbox, altura_hitbox)

        # Verificação de colisão com o alvo
        if hitbox.colliderect(alvo.rect):
            # Aplicar Dano
            if tipo == "soco":
                alvo.vida -= 100
            elif tipo == "chute":
                alvo.vida -= 8
            
            # ATIVAR KNOCKBACK E ESTADO DE HIT NO ALVO
            alvo.hit = True
            alvo.tempo_hit = pygame.time.get_ticks()
            
            # Se o atacante estiver à esquerda, empurra para a direita, senão para esquerda
            if self.rect.centerx < alvo.rect.centerx:
                alvo.rect.x += forca_knockback
            else:
                alvo.rect.x -= forca_knockback
            
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
                    if self.action == "soco" or self.action == "chute":
                        self.atacando = False
                    self.frame_index = 0

    def reset(self, x, y):
        self.vida = self.vida_maxima
        self.vivo = True
        self.hit = False
        self.atacando = False
        self.pulando = False
        self.vel_y = 0
        self.rect.x = x
        self.rect.y = y
        self.set_action("parado")

    def desenho(self, screen):
        self.atualizar_animacao()
        img = pygame.transform.flip(self.image, self.flip, False)
        
        pos_x = self.rect.x
        pos_y = self.rect.y

        # --- AJUSTES PLAYER 1 ---
        if self.jogador == 1:
            if self.action in ["parado", "soco", "chute"]:
                pos_y += 10
            # Se quiser alinhar o soco lateralmente (já que tem off_x=5):
            if self.action == "soco" and not self.flip:
                pos_x += 5

        # --- AJUSTES PLAYER 2 ---
        else:
            # Ajuste Vertical (Altura)
            if self.action in ["pulando", "chute"]:
                pos_y += 10
            elif self.action == "morte":
                pos_y += 5
            
            # Ajuste Horizontal (Largura)
            if not self.flip:
                if self.action == "parado":
                    pos_x += 10
                elif self.action in ["soco", "morte", "pulando"]:
                    pos_x += 5
                elif self.action == "chute":
                    pos_x += 3

        screen.blit(img, (pos_x, pos_y))