import pygame
import random

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load('imgs/pipe.png'))


class Cano:
    DISTANCIA = 200
    ALTURA = IMAGEM_CANO.get_height()  # the width of the pipe
    LARGURA = IMAGEM_CANO.get_width()  # the length of the pipe

    def __init__(self, x, velocidade=5) -> None:
        self.x = x
        self.altura = 0
        self.subida = bool(random.getrandbits(1))
        self.descida = not self.subida
        self.max = 0
        self.velocidade = velocidade

        # Posições do canos
        self.pos_top = 0
        self.pos_base = 0

        self.CANO_CIMA = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO

        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        # intervalo está entre 50 e 450 para surgimento do cano
        self.altura = random.randrange(50, 450)
        self.pos_top = self.altura - self.ALTURA
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self, cenario):
        self.x -= self.velocidade
        # Verifica o cenario atual
        if cenario > 1:
            velocidade = 2
            if self.subida:
                self.pos_top -= velocidade
                self.pos_base -= velocidade
                if (self.pos_top + self.ALTURA) <= 100:
                    self.subida = False
                    self.descida = True

            if self.descida:
                self.pos_top += velocidade
                self.pos_base += velocidade
                if self.pos_base >= 600:
                    self.subida = True
                    self.descida = False

    def acelerar(self, timesteps):
        '''
        Aumenta a velocidade com que o cano se move a cada chamada
        '''
        if self.velocidade <= 7:
            self.velocidade += 0.01*timesteps
        print(self.velocidade)

    def desenhar(self, tela):
        # Desenha o cano superior
        tela.blit(self.CANO_CIMA, (self.x, self.pos_top))
        # Desenha o cano inferior
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        top_mask = pygame.mask.from_surface(self.CANO_CIMA)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_top = (self.x - passaro.x, self.pos_top - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(top_mask, distancia_top)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if topo_ponto or base_ponto:
            return True
        return False
