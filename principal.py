import pygame
from personagens import Personagens

pygame.init()

# Criação da Janela
tela_largura = 1000
tela_altura = 563
screen = pygame.display.set_mode((tela_largura, tela_altura))

#definir taxa de quadros
clock = pygame.time.Clock()
fps = 60

# Nome do Jogo
pygame.display.set_caption('Pixel Fight')

# Plano de Andamento
def desenho_fundo():
    plano_andamento = pygame.image.load("Andamento.png")
    screen.blit(plano_andamento, (0, 0))

# criador de duas instâncias dos personagens
personagem_1 = Personagens(200, 260)
personagem_2 = Personagens(700, 260)

# game loop
andamento = True
while andamento:

    clock.tick(fps)

# desenho do fundo de andamento
    desenho_fundo()

# movimentação
    personagem_1.move(tela_largura, tela_altura, screen, personagem_2)
    personagem_2.move(tela_largura, tela_altura, screen, personagem_1)

# desenho dos personagens
    personagem_1.desenho(screen)
    personagem_2.desenho(screen)


# fechamento
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            andamento = False

# atualizão do display
    pygame.display.update()

# Desenvolvimento 1


pygame.quit()
