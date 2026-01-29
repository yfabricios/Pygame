import pygame
from personagens import Personagens

pygame.init()

# --------------------------------------------------
# Janela
tela_largura = 1000
tela_altura = 600
screen = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption("Pixel Fight")

# --------------------------------------------------
# Cores
ciano = (0, 200, 200)
branco = (255, 255, 255)
preto = (0, 0, 0)
amarelo = (255, 255, 0)
vermelho = (255, 0, 0)
azul = (0, 0, 255)
cinza = (235, 197, 197)
cinza_claro = (200, 200, 200)

# --------------------------------------------------
# Imagens
plano_andamento = pygame.image.load("Andamento.png").convert()
plano_menu = pygame.image.load("Menu.png").convert()
escala_menu = pygame.transform.scale(plano_menu, (tela_largura, tela_altura))

# --------------------------------------------------
# Variáveis do jogo
intro_contador = 5
last_contador_uptade = pygame.time.get_ticks()
mostrar_fight = False

pontuacao = [0, 0]
round_fim = False
round_contador = 2000
round_fim_tempo = 0

# Variáveis para a vitória final
vencedor_texto = ""
tempo_vitoria_final = 0

# --------------------------------------------------
# Fontes
contador_fonte = pygame.font.Font("Minecraft.ttf", 80)
pontuacao_fonte = pygame.font.Font("Minecraft.ttf", 30)
fonte = pygame.font.Font("Minecraft.ttf", 40)
vitoria_fonte = pygame.font.Font("Minecraft.ttf", 80)

# --------------------------------------------------
# Funções
def desenho_texto(texto, fonte, cor, x, y):
    img = fonte.render(texto, True, cor, cinza)
    screen.blit(img, (x, y))

def tela_menu():
    screen.blit(escala_menu, (0, 0))
    posicao_mouse = pygame.mouse.get_pos()

    if botao_jogar.collidepoint(posicao_mouse):
        cor_jogar = cinza_claro
    else:
        cor_jogar = branco 
        
    if botao_sair.collidepoint(posicao_mouse):
        cor_sair = cinza_claro
    else:
        cor_sair = branco

    pygame.draw.rect(screen, cor_jogar, botao_jogar)
    pygame.draw.rect(screen, cor_sair, botao_sair)

    texto_jogar = fonte.render("JOGAR", True, preto)
    texto_sair = fonte.render("SAIR", True, preto)

    screen.blit(texto_jogar, texto_jogar.get_rect(center=botao_jogar.center))
    screen.blit(texto_sair, texto_sair.get_rect(center=botao_sair.center))

def tela_de_andamento():
    screen.blit(plano_andamento, (0, 0))

def desenhar_barra_vida(vida, x, y):
    proporcao = max(0, vida / 100) # Garante que a barra não fique negativa
    pygame.draw.rect(screen, branco, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, vermelho, (x, y, 400, 30))
    pygame.draw.rect(screen, amarelo, (x, y, 400 * proporcao, 30))

# --------------------------------------------------
# Estados
MENU = 0
JOGO = 1
VITORIA_FINAL = 2 
estado = MENU

# --------------------------------------------------
# Botões
botao_jogar = pygame.Rect(400, 220, 200, 60)
botao_sair = pygame.Rect(400, 300, 200, 60)

# --------------------------------------------------
# Clock
clock = pygame.time.Clock()
fps = 60

# --------------------------------------------------
# Personagens
plazer_sheet = pygame.image.load("Plazer1.png").convert_alpha()
reihard_sheet = pygame.image.load("Reihard2.png").convert_alpha()

personagem_1 = Personagens(100, 215, 1, plazer_sheet, 100)
personagem_2 = Personagens(800, 215, 2, reihard_sheet, 100)

# --------------------------------------------------
# Game loop
rodando = True
while rodando:
    clock.tick(fps)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if estado == MENU and evento.type == pygame.MOUSEBUTTONDOWN:
            if botao_jogar.collidepoint(evento.pos):
                # Resetar pontos ao clicar em Jogar
                pontuacao = [0, 0]
                estado = JOGO
            if botao_sair.collidepoint(evento.pos):
                rodando = False

    if estado == MENU:
        tela_menu()

    elif estado == JOGO:
        tela_de_andamento()

        desenhar_barra_vida(personagem_1.vida, 20, 20)
        desenhar_barra_vida(personagem_2.vida, 580, 20)

        desenho_texto(f"P1: {pontuacao[0]}", pontuacao_fonte, azul, 20, 60)
        desenho_texto(f"R2: {pontuacao[1]}", pontuacao_fonte, vermelho, 910, 60)

        # ---------------- CONTADOR / FIGHT ----------------
        if intro_contador > 0:
            texto = contador_fonte.render(str(intro_contador), True, vermelho)
            screen.blit(texto, texto.get_rect(center=(tela_largura // 2, tela_altura // 5)))

            if pygame.time.get_ticks() - last_contador_uptade >= 1000:
                intro_contador -= 1
                last_contador_uptade = pygame.time.get_ticks()

        elif intro_contador == 0:
            texto = contador_fonte.render("FIGHT!", True, vermelho)
            screen.blit(texto, texto.get_rect(center=(tela_largura // 2, tela_altura // 5)))

            if not mostrar_fight:
                mostrar_fight = True
                last_contador_uptade = pygame.time.get_ticks()

            if pygame.time.get_ticks() - last_contador_uptade >= 1000:
                intro_contador = -1

        else:
            personagem_1.move(tela_largura, tela_altura, personagem_2, round_fim)
            personagem_2.move(tela_largura, tela_altura, personagem_1, round_fim)

        personagem_1.desenho(screen)
        personagem_2.desenho(screen)

        # ---------------- FIM DE ROUND / JOGO ----------------
        if not round_fim:
            if not personagem_1.vivo:
                pontuacao[1] += 1
                round_fim = True
                round_fim_tempo = pygame.time.get_ticks()
            elif not personagem_2.vivo:
                pontuacao[0] += 1
                round_fim = True
                round_fim_tempo = pygame.time.get_ticks()
            
            # Verificar se alguém atingiu 3 pontos
            if pontuacao[0] >= 3:
                vencedor_texto = "PLAZER1 WINS!"
                tempo_vitoria_final = pygame.time.get_ticks()
                estado = VITORIA_FINAL
            elif pontuacao[1] >= 3:
                vencedor_texto = "REIHARD2 WINS!"
                tempo_vitoria_final = pygame.time.get_ticks()
                estado = VITORIA_FINAL

        else:
            # Exibe mensagem de vitória do round enquanto espera o reset
            texto_round = vitoria_fonte.render("VICTORY", True, vermelho)
            screen.blit(texto_round, texto_round.get_rect(center=(tela_largura // 2, tela_altura // 5)))

            if pygame.time.get_ticks() - round_fim_tempo >= round_contador:
                round_fim = False
                intro_contador = 5
                mostrar_fight = False
                last_contador_uptade = pygame.time.get_ticks()
                
                personagem_1.reset(100, 215)
                personagem_2.reset(800, 215)

    # ---------------- TELA DE VITÓRIA FINAL (3 PONTOS) ----------------
    elif estado == VITORIA_FINAL:
        screen.blit(escala_menu, (0, 0)) # Fundo do menu
        
        texto_campeao = vitoria_fonte.render(vencedor_texto, True, amarelo)
        rect_campeao = texto_campeao.get_rect(center=(tela_largura // 2, tela_altura // 2))
        screen.blit(texto_campeao, rect_campeao)

        # Espera 5 segundos antes de voltar ao menu
        if pygame.time.get_ticks() - tempo_vitoria_final >= 5000:
            # Reset completo para voltar ao menu
            intro_contador = 5
            mostrar_fight = False
            round_fim = False
            personagem_1.reset(100, 215)
            personagem_2.reset(800, 215)
            estado = MENU

    pygame.display.update()

pygame.quit()