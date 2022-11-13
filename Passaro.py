import pygame


class Passaro:
    # atributos
    IMGS = [pygame.transform.scale2x(pygame.image.load(
        f'imgs/bird{x}.png')) for x in range(1, 4)]
    ROTAÇÃO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5
    LARGURA = IMGS[0].get_width()
    ALTURA = IMGS[0].get_height()

    def __init__(self, x, y) -> None:
        # posição inicial do passaro
        self.x = x
        self.y = y
        self.imagem = self.IMGS[0]
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.img_count = 0

    def pular(self) -> None:
        self.velocidade = -10.5  # velocidade do pulo
        self.tempo = 0  # ao pular o tempo volta a xero
        self.altura = self.y

    def mover(self) -> None:

        self.tempo += 1
        # Calculando deslocamento a partida da formula de deslocamento
        # d = vt + 1/2at^2
        deslocamento = self.velocidade * self.tempo + 1.5 * (self.tempo**2)

        # Restringir o deslocamento no caso de o passaro estiver descendo muito rapido
        if deslocamento > 12:
            deslocamento = 12

        # if deslocamento < 0:
        #     deslocamento -= 2

        # calculando a nova posição y do pássaro após o deslocamento
        self.y += deslocamento

        # Angulo
        if deslocamento < 0 or self.y < self.altura + 50:
            # se o grau de voo for menor que o grau máx de voo para cima
            if self.angulo < self.ROTAÇÃO_MAXIMA:
                self.angulo = self.ROTAÇÃO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # definir imagem
        self.img_count += 1

        # se o pássaro não estiver caindo, ele bate as asas
        # repetindo as 3 imagens de pássaros para imitar o bater de suas asas
        if self.img_count < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.img_count < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.img_count < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.img_count < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        else:
            self.imagem = self.IMGS[0]
            self.img_count = 0
        # se cair
        # if self.angulo <= -80:
        #     self.imagem = self.IMGS[1]
        #     self.img_count = self.TEMPO_ANIMACAO*2

        # Desenhar
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_img = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_img)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)
