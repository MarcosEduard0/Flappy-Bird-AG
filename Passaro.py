import pygame


class Passaro:
    IMGS = [
        pygame.transform.scale2x(pygame.image.load('imgs/bird1.png')),
        pygame.transform.scale2x(pygame.image.load('imgs/bird2.png')),
        pygame.transform.scale2x(pygame.image.load('imgs/bird3.png')),
    ]
    IMGS = [pygame.transform.scale2x(pygame.image.load(
        f'imgs/bird{x}.png')) for x in range(1, 4)]

    # animação
    ROTAÇÃO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.img_count = 0
        self.imagem = self.IMGS[0]

    def pular(self) -> None:
        '''
            Faz o passaro pular
        '''
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self) -> None:
        '''
            Movimentos do passaro
        '''
        # Calculando deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # Restringir o deslocamento
        if deslocamento >= 16:
            deslocamento = 16

        if deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # Angulo
        if deslocamento < 0 or self.y < self.altura + 50:
            if self.angulo < self.ROTAÇÃO_MAXIMA:
                self.angulo = self.ROTAÇÃO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # definir imagem
        self.img_count += 1

        if self.img_count <= self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.img_count <= self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.img_count <= self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.img_count <= self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.img_count == self.TEMPO_ANIMACAO*4+1:
            self.imagem = self.IMGS[0]
            self.img_count = 0

        # se cair
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.img_count = self.TEMPO_ANIMACAO*2

        # Desenhar
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_img = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_img)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        '''
            Teste de colisão
        '''
        return pygame.mask.from_surface(self.imagem)
