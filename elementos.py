import pygame
import random
from abc import ABCMeta, abstractmethod
from main import *
from config import *


class ElementoJogo(metaclass=ABCMeta):
    @abstractmethod
    def desenhar(self, tela):
        pass

    @abstractmethod
    def calcular_regras(self):
        pass

    @abstractmethod
    def processar_eventos(self, events):
        pass


class Cenario(ElementoJogo):
    def __init__(self, pacman, fonte):
        self.pacman = pacman
        self.fonte = fonte
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
        img_pontos = self.fonte.render("Score: {}".format(self.pontos), True, AZUL)
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

    def processar_eventos(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit()


class Pastilha(ElementoJogo):
    def __init__(self, linha, coluna, tela):
        self.tamanho = TAMANHO // 10
        self.centro_x = coluna * TAMANHO + TAMANHO // 2
        self.centro_y = linha * TAMANHO + TAMANHO // 2
        self.desenhar(tela)

    def desenhar(self, tela):
        pygame.draw.circle(tela, BRANCO, (self.centro_x, self.centro_y), self.tamanho, 0)

    def calcular_regras(self):
        pass

    def processar_eventos(self, events):
        pass


class Pilula(ElementoJogo):
    def __init__(self, linha, coluna, tela):
        self.tamanho = TAMANHO // 5
        self.centro_x = coluna * TAMANHO + TAMANHO // 2
        self.centro_y = linha * TAMANHO + TAMANHO // 2
        self.desenhar(tela)

    def desenhar(self, tela):
        pygame.draw.circle(tela, VERMELHO, (self.centro_x, self.centro_y), self.tamanho, 0)

    def calcular_regras(self):
        pass

    def processar_eventos(self, events):
        pass


class Pacman(ElementoJogo):
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
                    self.vel_y = -VELOCIDADE
                if event.key == pygame.K_DOWN:
                    self.vel_y = VELOCIDADE
                if event.key == pygame.K_LEFT:
                    self.vel_x = -VELOCIDADE
                    self.ori_x = -1 if 1 else self.ori_x
                if event.key == pygame.K_RIGHT:
                    self.vel_x = VELOCIDADE
                    self.ori_x = 1 if -1 else self.ori_x
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.vel_y = 0
                if event.key == pygame.K_DOWN:
                    self.vel_y = 0
                if event.key == pygame.K_LEFT:
                    self.vel_x = 0
                if event.key == pygame.K_RIGHT:
                    self.vel_x = 0

    def processar_eventos_mouse(self, events):
        delay = 100
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                self.coluna = (mouse_x - self.centro_x) / delay
                self.linha = (mouse_y - self.centro_y) / delay


class Fantasma(ElementoJogo):
    def __init__(self, cor, lin, col):
        self.cor = cor
        self.raio = TAMANHO // 2
        self.coluna = col
        self.linha = lin
        self.centro_x = self.coluna * TAMANHO + self.raio
        self.centro_y = self.linha * TAMANHO + self.raio
        self.matriz = MATRIZ
        self.vel = VELOCIDADE
        self.direcao = 0

    def get_direcoes(self, lin, col):
        direcoes = []
        if self.matriz[int(lin - 1)][int(col)] != 2:
            direcoes.append(ACIMA)
        if self.matriz[int(lin)][int(col + 1)] != 2:
            direcoes.append(DIREITA)
        if self.matriz[int(lin + 1)][int(col)] != 2:
            direcoes.append(ABAIXO)
        if self.matriz[int(lin)][int(col - 1)] != 2:
            direcoes.append(ESQUERDA)
        return direcoes

    def calcular_regras(self):
        # Verificar se não está em corredor ou beco
        direcoes = self.get_direcoes(self.linha, self.coluna)
        if len(direcoes) > 1:
            corredor = abs(direcoes[1] - direcoes[0]) == 2
            if len(direcoes) == 2 and corredor:
                self.direcao = self.direcao
            else:
                self.direcao = random.choice(direcoes)

        # Realizar movimento
        if self.direcao == ACIMA:
            self.linha -= self.vel
        if self.direcao == DIREITA:
            self.coluna += self.vel
        if self.direcao == ABAIXO:
            self.linha += self.vel
        if self.direcao == ESQUERDA:
            self.coluna -= self.vel

    def desenhar(self, tela):
        self.tela = tela
        self.centro_x = self.coluna * TAMANHO + self.raio
        self.centro_y = self.linha * TAMANHO + self.raio
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

    def processar_eventos(self, events):
        pass
