import pygame

IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load('imgs/base.png'))


class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y) -> None:
        # como a imagem do piso não é grande o suficiente para preencher a tela, precisamos de 2 imagens
        # essas 2 imagens têm posição inicial diferente, mas têm a mesma posição y
        self.y = y
        self.x1 = 0  # posição incial do chao 1
        self.x2 = self.LARGURA  # posicao logos apos o chao 1

    def acelerar(self):
        '''
        Aumenta a velocidade com que o chão se move a cada chamada
        '''
        if self.VELOCIDADE <= 6:
            self.VELOCIDADE += 0.01

    def mover(self, cenario=1):
        # movendo o chao
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        # reposicionando o chao
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

        # Verifica o cenario atual
        if cenario > 2:
            self.acelerar()

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))
