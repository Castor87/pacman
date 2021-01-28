import pygame
from config import *


class Cenario:
    def __init__(self, pacman):
        self.pacman = pacman
        self.pontos = 0
        self.tamanho = TAMANHO
        self.matriz = MATRIZ

    def desenhar(self, tela):
        for numero_linha, linha in enumerate(self.matriz):
            for numero_coluna, coluna in enumerate(linha):
                if coluna == 2:
                    x = numero_coluna * self.tamanho
                    y = numero_linha * self.tamanho
                    pygame.draw.rect(tela, AZUL, (x, y, self.tamanho, self.tamanho), 0)
                if coluna == 1:
                    Pastilha(numero_linha, numero_coluna, tela)
                if coluna == 5:
                    Pilula(numero_linha, numero_coluna, tela)

    def desenhar_pontuacao(self, tela):
        self.tela = tela
        pontos_x = LARGURA // 2
        pontos_y = 0
        img_pontos = fonte.render("Score: {}".format(self.pontos), True, AZUL)
        pontos_largura = img_pontos.get_width()
        self.tela.blit(img_pontos, (pontos_x - pontos_largura // 2, pontos_y))

    def calcular_regras(self):
        col = self.pacman.col_intencao
        lin = self.pacman.lin_intencao
        if 0 <= col <= COLUNAS and 0 <= lin <= LINHAS:
            if self.matriz[lin][col] != 2:
                self.pacman.aceitar_movimento()
                if self.matriz[lin][col] == 1:
                    self.pontos += 1
                    self.matriz[lin][col] = 0


class Pastilha:
    def __init__(self, linha, coluna, tela):
        self.tamanho = TAMANHO // 10
        self.centro_x = coluna * TAMANHO + TAMANHO // 2
        self.centro_y = linha * TAMANHO + TAMANHO // 2
        self.desenhar(tela)

    def desenhar(self, tela):
        pygame.draw.circle(tela, BRANCO, (self.centro_x, self.centro_y), self.tamanho, 0)


class Pilula:
    def __init__(self, linha, coluna, tela):
        self.tamanho = TAMANHO // 5
        self.centro_x = coluna * TAMANHO + TAMANHO // 2
        self.centro_y = linha * TAMANHO + TAMANHO // 2
        self.desenhar(tela)

    def desenhar(self, tela):
        pygame.draw.circle(tela, VERMELHO, (self.centro_x, self.centro_y), self.tamanho, 0)


class Pacman:
    def __init__(self):
        self.coluna = 1
        self.linha = 2
        self.raio = TAMANHO // 2
        self.centro_x = self.coluna * TAMANHO + self.raio
        self.centro_y = self.linha * TAMANHO + self.raio
        self.tamanho = TAMANHO
        self.vel_x = 0
        self.vel_y = 0
        self.ori_x = 1
        self.col_intencao = self.coluna
        self.lin_intencao = self.linha

    def calcular_regras(self):  # Semelhante ao método Update

        self.col_intencao = self.coluna + self.vel_x
        self.lin_intencao = self.linha + self.vel_y
        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)

    def aceitar_movimento(self):
        self.coluna = self.col_intencao
        self.linha = self.lin_intencao

    def desenhar(self, tela):

        # Corpo do Pacman
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio, 0)

        # Boca do Pacman
        boca_centro = (self.centro_x, self.centro_y)
        boca_cima = (self.centro_x + (self.raio - 1 * self.ori_x) * self.ori_x, self.centro_y - self.raio)
        boca_baixo = (self.centro_x + (self.raio - 1 * self.ori_x) * self.ori_x, self.centro_y + self.raio)
        pygame.draw.polygon(tela, PRETO, [boca_centro, boca_cima, boca_baixo], 0)

        # Olho do Pacman
        olho_x = self.centro_x
        olho_y = self.centro_y - self.raio // 2
        olho_raio = self.raio // 6
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

    def processar_eventos(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman.vel_y = -VELOCIDADE
                if event.key == pygame.K_DOWN:
                    pacman.vel_y = VELOCIDADE
                if event.key == pygame.K_LEFT:
                    pacman.vel_x = -VELOCIDADE
                    pacman.ori_x = -1 if 1 else pacman.ori_x
                if event.key == pygame.K_RIGHT:
                    pacman.vel_x = VELOCIDADE
                    pacman.ori_x = 1 if -1 else pacman.ori_x
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    pacman.vel_y = 0
                if event.key == pygame.K_DOWN:
                    pacman.vel_y = 0
                if event.key == pygame.K_LEFT:
                    pacman.vel_x = 0
                if event.key == pygame.K_RIGHT:
                    pacman.vel_x = 0

    def processar_eventos_mouse(self, events):
        delay = 100
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                self.coluna = (mouse_x - self.centro_x) / delay
                self.linha = (mouse_y - self.centro_y) / delay


if __name__ == "__main__":

    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA), 0)
    fonte = pygame.font.SysFont("calibri", TAMANHO, True, False)

    pacman = Pacman()
    cenario = Cenario(pacman)

    while True:

        # Parte 1 - Calcular regras
        pacman.calcular_regras()
        cenario.calcular_regras()

        # Parte 2 - Desenhar tela
        tela.fill(PRETO)
        cenario.desenhar(tela)
        cenario.desenhar_pontuacao(tela)
        pacman.desenhar(tela)
        pygame.display.update()
        pygame.time.delay(100)

        # Parte 3 - Capturar eventos
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit()
            pacman.processar_eventos(events)
