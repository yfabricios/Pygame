import pygame
from personagens import Personagens

pygame.init()

# Criação da Janela
tela_largura = 1000
tela_altura = 563
screen = pygame.display.set_mode((tela_largura, tela_altura))

# cores
ciano = (0, 200, 200)
branco = (255, 255, 255)
preto = (0, 0, 0)
amarelo = (255, 255, 0)
vermelho = (255, 0, 0)

#definir variaveis dos personagens
plazer1_largura = 80
plazer1_escala = 4
plazer1_offset = [72, 56]
plazer1_data = [plazer1_largura, plazer1_escala, plazer1_offset]
reihard2_largura = 80
reihard2_escala = 4
reihard2_offset = [112, 107]
reihard2_data = [reihard2_largura, reihard2_escala, reihard2_offset]

# Fonte
fonte = pygame.font.SysFont(None, 40)

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
    desenhar_barra_vida(personagem_1.vida, 20, 20)
    desenhar_barra_vida(personagem_2.vida, 580, 20)

#spritesheets
plazer1_sheets = pygame.image.load("Plazer1.png").convert()
reihard2_sheets = pygame.image.load("Reihard2.png").convert()

#definir numero de passos de cada animação
plazer1_anima_passos = [4, 5, 6, 3, 6, 3, 3, 4, 5, 3]
reihard2_anima_passos = [6, 3, 6, 4, 3, 3, 5, 4, 3, 6]

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
personagem_1 = Personagens(200, 260, False, plazer1_data, plazer1_sheets, plazer1_anima_passos)
personagem_2 = Personagens(700, 260, True, reihard2_data, reihard2_sheets, reihard2_anima_passos)

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
        
# movimentação (da tela de andamento)
        personagem_1.move(tela_largura, tela_altura, screen, personagem_2)
        personagem_2.move(tela_largura, tela_altura, screen, personagem_1)

# desenho dos personagens (da tela de andamento)
        personagem_1.desenho(screen)
        personagem_2.desenho(screen)

# atualizão do display
    pygame.display.update()

pygame.quit()