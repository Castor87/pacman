import pygame
from config import *
from elementos import *

pygame.init()


class Fantasma:
    def __init__(self, tela, cor, x, y):
        self.tela = tela
        self.cor = cor
        self.raio = TAMANHO // 2
        self.centro_x = x
        self.centro_y = y

    def desenhar(self):
        # Cabeça do fantasma
        pygame.draw.circle(self.tela, self.cor, (self.centro_x, self.centro_y), self.raio, 0)

        # Corpo do fantasma
        pygame.draw.rect(self.tela, self.cor,
                         (self.centro_x - self.raio, self.centro_y, self.raio * 2, self.raio), 0)

        # Olho esquerdo do fantasma
        pygame.draw.circle(self.tela, BRANCO,
                           (self.centro_x - self.raio // 3, self.centro_y - self.raio // 2),
                           self.raio // 4, 0)
        pygame.draw.circle(self.tela, AZUL,
                           (self.centro_x - self.raio // 3, self.centro_y - self.raio // 2),
                           self.raio // 7, 0)
        # Olho direito do fantasma
        pygame.draw.circle(self.tela, BRANCO,
                           (self.centro_x + self.raio // 3, self.centro_y - self.raio // 2),
                           self.raio // 4, 0)
        pygame.draw.circle(self.tela, AZUL,
                           (self.centro_x + self.raio // 3, self.centro_y - self.raio // 2),
                           self.raio // 7, 0)


tela = pygame.display.set_mode((LARGURA, ALTURA), 0)
fantasma_verm = Fantasma(tela, VERMELHO, 60, 60)
fantasma_cian = Fantasma(tela, CIANO, 84, 60)
fantasma_larj = Fantasma(tela, LARANJA, 108, 60)
fantasma_mage = Fantasma(tela, MAGENTA, 132, 60)
pacman = Pacman()

if __name__ == "__main__":

    while True:

        tela.fill(PRETO)
        fantasma_verm.desenhar()
        fantasma_cian.desenhar()
        fantasma_larj.desenhar()
        fantasma_mage.desenhar()
        pacman.desenhar(tela)
        pygame.display.update()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit()
