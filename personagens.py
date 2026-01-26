import pygame

class Personagens():
    def __init__(self, x, y, jogador, sprite_sheet, vida):
        self.jogador = jogador
        self.sprite_sheet = sprite_sheet
        self.vida = vida

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

    # --------------------------------------------------

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

    # --------------------------------------------------

    def move(self, largura, altura, screen, alvo, round_fim):
        if round_fim:
            self.vel_y = 0
            self.pulando = False
            self.rect.bottom = 395
            return

        if not self.vivo:
            return

        velocidade = 6
        dx = 0
        dy = 0

        teclas = pygame.key.get_pressed()
        movendo = False

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
                    self.set_action("pulando")

                if teclas[pygame.K_r]:
                    self.atacar("soco", alvo)
                elif teclas[pygame.K_t]:
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
                    self.set_action("pulando")

                if teclas[pygame.K_o]:
                    self.atacar("soco", alvo)
                elif teclas[pygame.K_p]:
                    self.atacar("chute", alvo)

        if movendo and not self.pulando and not self.atacando:
            self.set_action("andando")
        elif not self.pulando and not self.atacando:
            self.set_action("parado")

        self.vel_y += 1
        dy += self.vel_y

        chao = 395
        if self.rect.bottom + dy > chao:
            dy = chao - self.rect.bottom
            self.vel_y = 0
            self.pulando = False

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > largura:
            self.rect.right = largura

        if self.jogador == 1:
            self.flip = self.rect.centerx > alvo.rect.centerx
        else:
            self.flip = self.rect.centerx < alvo.rect.centerx

    # --------------------------------------------------

    def atacar(self, tipo, alvo):
        tempo_atual = pygame.time.get_ticks()

        if self.atacando:
            return

        if tempo_atual - self.ultimo_ataque < self.tempo_cooldown:
            return

        self.atacando = True
        self.ultimo_ataque = tempo_atual
        self.frame_index = 0
        self.set_action(tipo)

        # -------- HITBOX CORRETA PARA CADA SPRITE BASE
        if self.jogador == 1:
            offset = 40 if not self.flip else -40
        else:
            offset = -40 if not self.flip else 40

        hitbox = pygame.Rect(
            self.rect.centerx + offset,
            self.rect.y + 40,
            40,
            80
        )

        if hitbox.colliderect(alvo.rect):
            alvo.vida -= 10
            if alvo.vida <= 0:
                alvo.vivo = False
                alvo.atacando = False
                alvo.pulando = False
                alvo.vel_y = 0
                alvo.set_action("morte")

    # --------------------------------------------------

    def set_action(self, nova):
        if self.action != nova:
            self.action = nova
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    # --------------------------------------------------

    def atualizar_animacao(self):
        if not self.vivo:
            self.image = self.animacoes["morte"][0]
            return

        tempo = 180
        self.image = self.animacoes[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > tempo:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

            if self.frame_index >= len(self.animacoes[self.action]):
                self.frame_index = 0
                if self.action in ["soco", "chute"]:
                    self.atacando = False
                    self.set_action("parado")

    # --------------------------------------------------

    def desenho(self, screen):
        self.atualizar_animacao()
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, self.rect)
