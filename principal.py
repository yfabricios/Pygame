import pygame
from personagens import Personagens

pygame.init()

# Criação da Janela
tela_largura = 1000
tela_altura = 600
screen = pygame.display.set_mode((tela_largura, tela_altura))

# cores
ciano = (0, 200, 200)
branco = (255, 255, 255)
preto = (0, 0, 0)
amarelo = (255, 255, 0)
vermelho = (255, 0, 0)

# carregando vitoria imagem
vitoria_img = pygame.image.load("Vitoria.png").convert_alpha()

# definir as variaveis do jogo
intro_contador = 5
last_contador_uptade = pygame.time.get_ticks()
pontuacao = [0, 0] # [p1, p2]
round_fim = False
round_contador = 2000

# Fonte
contador_fonte = pygame.font.Font("Minecraft.ttf", 80)
pontuacao_fonte = pygame.font.Font("Minecraft.ttf", 30)
fonte = pygame.font.SysFont(None, 40)

# função para desenhar o texto
def desenho_texto(texto, fonte, texto_cor, x, y):
    img = fonte.render(texto, True, texto_cor)
    screen.blit(img, (x, y))

# Estados
menu = 0
jogo = 1
estado = menu

# Botões
botao_jogar = pygame.Rect(400, 220, 200, 60)
botao_sair = pygame.Rect(400, 300, 200, 60)

# tela de menu
def tela_menu():
    screen.fill(ciano)

    pygame.draw.rect(screen, branco, botao_jogar)
    pygame.draw.rect(screen, branco, botao_sair)

    texto_jogar = fonte.render("JOGAR", True, preto)
    texto_sair = fonte.render("SAIR", True, preto)

    screen.blit(texto_jogar, texto_jogar.get_rect(center=botao_jogar.center))
    screen.blit(texto_sair, texto_sair.get_rect(center=botao_sair.center))


# NÃO TIRAR OS COMENTÁRIOS ABAIXO, SERVEM PARA FUTURAS TELAS DE FUNDO***************************
# fundo_menu = pygame.image.load("menu.png").convert()
# fundo_menu = pygame.transform.scale(fundo_menu, (tela_largura, tela_altura))

# Plano de Andamento
def tela_de_andamento():
    plano_andamento = pygame.image.load("plano_de_andamento.png").convert()
    screen.blit(plano_andamento, (0, 0))

# Desenhar barras de vida
def desenhar_barra_vida(vida, x, y):
    proporcao = vida / 100
    pygame.draw.rect(screen, branco, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, vermelho, (x, y, 400, 30))
    pygame.draw.rect(screen, amarelo, (x, y, 400 * proporcao, 30))

# definir taxa de quadros
clock = pygame.time.Clock()
fps = 60

# Nome do Jogo
pygame.display.set_caption('Pixel Fight')

# criador de duas instâncias dos personagens
personagem_1 = Personagens(1, 200, 215)
personagem_2 = Personagens(2, 700, 215)

# game loop
andamento = True
while andamento:

# tempo de quadros
    clock.tick(fps)

# fechamento
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            andamento = False

        if estado == menu and evento.type == pygame.MOUSEBUTTONDOWN:
            if botao_jogar.collidepoint(evento.pos):
                estado = jogo
            if botao_sair.collidepoint(evento.pos):
                andamento = False

# chamando tela menu
    if estado == menu:
        tela_menu()
# chamando tela de andamento
    elif estado == jogo:
        tela_de_andamento()

# desenho da barra de vida
        desenhar_barra_vida(personagem_1.vida, 20, 20)
        desenhar_barra_vida(personagem_2.vida, 580, 20)
        desenho_texto("P1: " + str(pontuacao[0]), pontuacao_fonte, amarelo, 20, 60)
        desenho_texto("R2: " + str(pontuacao[1]), pontuacao_fonte, amarelo, 580, 60)

# atualização do cronometro
        if intro_contador <= 0:
    # movimentação (da tela de andamento)
            personagem_1.move(tela_largura, tela_altura, screen, personagem_2, round_fim)
            personagem_2.move(tela_largura, tela_altura, screen, personagem_1, round_fim)
        else:
    # atualizador do contador do cronometro
            desenho_texto(str(intro_contador), contador_fonte, vermelho, tela_largura / 2, tela_altura / 5)
    # atualização do contador do cronometro
            if (pygame.time.get_ticks() - last_contador_uptade) >= 1000:
                intro_contador -= 1
                last_contador_uptade = pygame.time.get_ticks()

# desenho dos personagens (da tela de andamento)
        personagem_1.desenho(screen)
        personagem_2.desenho(screen)

# checar quando o player for derrotado
        if round_fim == False:
            if personagem_1.vida <= 0:
                personagem_1.vivo == False
                pontuacao[1] += 1
                round_fim = True
                round_fim_tempo = pygame.time.get_ticks()
            elif personagem_2.vida <= 0:
                personagem_2.vivo == False
                pontuacao[0] += 1
                round_fim = True
                round_fim_tempo = pygame.time.get_ticks()
        else:
    # exibição da imagem da vitoria
            screen.blit(vitoria_img, (360, 150))
            if pygame.time.get_ticks() - round_fim_tempo > round_contador:
                round_fim = False
                intro_contador = 3
                personagem_1 = Personagens(1, 200, 215)
                personagem_2 = Personagens(2, 700, 215)
# atualizão do display
    pygame.display.update()

pygame.quit()