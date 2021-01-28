import pygame
from config import *
from elementos import *

if __name__ == "__main__":

    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA), 0)
    fonte = pygame.font.SysFont("calibri", TAMANHO, True, False)

    pacman = Pacman()
    blinky = Fantasma(VERMELHO, 2, 26)  # Fantasma(VERMELHO, 15, 13)
    cenario = Cenario(pacman, fonte)

    while True:

        # Parte 1 - Calcular regras
        pacman.calcular_regras()
        cenario.calcular_regras()
        blinky.calcular_regras()
        direcoes = blinky.get_direcoes(blinky.linha, blinky.coluna)

        # Parte 2 - Desenhar tela
        tela.fill(PRETO)
        cenario.desenhar(tela)
        cenario.desenhar_pontuacao(tela)
        pacman.desenhar(tela)
        blinky.desenhar(tela)
        pygame.display.update()
        pygame.time.delay(100)

        # Parte 3 - Capturar eventos
        events = pygame.event.get()
        pacman.processar_eventos(events)
        cenario.processar_eventos(events)
