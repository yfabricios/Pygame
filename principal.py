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

# --------------------------------------------------
# Imagens (carregar UMA vez)
vitoria_img = pygame.image.load("Vitoria.png").convert_alpha()
plano_andamento = pygame.image.load("plano_de_andamento.png").convert()

# --------------------------------------------------
# Variáveis do jogo
intro_contador = 5
last_contador_uptade = pygame.time.get_ticks()
pontuacao = [0, 0]
round_fim = False
round_contador = 2000
round_fim_tempo = 0

# --------------------------------------------------
# Fontes
contador_fonte = pygame.font.Font("Minecraft.ttf", 80)
pontuacao_fonte = pygame.font.Font("Minecraft.ttf", 30)
fonte = pygame.font.SysFont(None, 40)

# --------------------------------------------------
# Funções
def desenho_texto(texto, fonte, cor, x, y):
    img = fonte.render(texto, True, cor)
    screen.blit(img, (x, y))

def tela_menu():
    screen.fill(ciano)
    pygame.draw.rect(screen, branco, botao_jogar)
    pygame.draw.rect(screen, branco, botao_sair)

    texto_jogar = fonte.render("JOGAR", True, preto)
    texto_sair = fonte.render("SAIR", True, preto)

    screen.blit(texto_jogar, texto_jogar.get_rect(center=botao_jogar.center))
    screen.blit(texto_sair, texto_sair.get_rect(center=botao_sair.center))

def tela_de_andamento():
    screen.blit(plano_andamento, (0, 0))

def desenhar_barra_vida(vida, x, y):
    proporcao = vida / 100
    pygame.draw.rect(screen, branco, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, vermelho, (x, y, 400, 30))
    pygame.draw.rect(screen, amarelo, (x, y, 400 * proporcao, 30))

# --------------------------------------------------
# Estados
MENU = 0
JOGO = 1
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
personagem_1 = Personagens(1, 200, 215)
personagem_2 = Personagens(2, 700, 215)

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
                estado = JOGO
            if botao_sair.collidepoint(evento.pos):
                rodando = False

    if estado == MENU:
        tela_menu()

    elif estado == JOGO:
        tela_de_andamento()

        # UI
        desenhar_barra_vida(personagem_1.vida, 20, 20)
        desenhar_barra_vida(personagem_2.vida, 580, 20)
        desenho_texto(f"P1: {pontuacao[0]}", pontuacao_fonte, amarelo, 20, 60)
        desenho_texto(f"P2: {pontuacao[1]}", pontuacao_fonte, amarelo, 580, 60)

        # Cronômetro inicial
        if intro_contador <= 0:
            personagem_1.move(tela_largura, tela_altura, screen, personagem_2, round_fim)
            personagem_2.move(tela_largura, tela_altura, screen, personagem_1, round_fim)
        else:
            texto = contador_fonte.render(str(intro_contador), True, vermelho)
            screen.blit(texto, texto.get_rect(center=(tela_largura // 2, tela_altura // 5)))

            if pygame.time.get_ticks() - last_contador_uptade >= 1000:
                intro_contador -= 1
                last_contador_uptade = pygame.time.get_ticks()

        # Desenho dos personagens
        personagem_1.desenho(screen)
        personagem_2.desenho(screen)

        # Checar fim do round
        if not round_fim:
            if personagem_1.vida <= 0:
                personagem_1.vivo = False
                pontuacao[1] += 1
                round_fim = True
                round_fim_tempo = pygame.time.get_ticks()

            elif personagem_2.vida <= 0:
                personagem_2.vivo = False
                pontuacao[0] += 1
                round_fim = True
                round_fim_tempo = pygame.time.get_ticks()
        else:
            screen.blit(vitoria_img, (360, 150))
            if pygame.time.get_ticks() - round_fim_tempo > round_contador:
                round_fim = False
                intro_contador = 3
                personagem_1 = Personagens(1, 200, 215)
                personagem_2 = Personagens(2, 700, 215)

    pygame.display.update()

pygame.quit()