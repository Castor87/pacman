import pygame

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

pygame.init()
tela = pygame.display.set_mode((800, 600), 0)

score = 0
fonte = pygame.font.SysFont("calibri", 24, bold=True, italic=False)

while True:

    texto = "Score: {}".format(score)
    img_texto = fonte.render(texto, True, BRANCO)

    tela.fill(PRETO)
    tela.blit(img_texto, (168, 433))
    pygame.draw.rect(tela, BRANCO, (0 + 5, 400, 800 - 10, 200 - 5), 5)
    pygame.draw.rect(tela, BRANCO, (38, 433, 100, 133), 0)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                score += 10
            if event.key == pygame.K_DOWN:
                score -= 10
