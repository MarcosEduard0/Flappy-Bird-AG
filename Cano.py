import pygame
import random

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load('imgs/pipe.png'))


class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x) -> None:
        self.x = x
        self.altura = 0

        # Posições do canos
        self.pos_top = 0
        self.pos_base = 0

        self.CANO_CIMA = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO

        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_top = self.altura - self.CANO_CIMA.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

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