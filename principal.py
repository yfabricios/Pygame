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