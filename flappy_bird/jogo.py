"""Simulação e renderização do jogo."""
import pygame
import neat
from .entidades.passaro import Passaro
from .entidades.cano import Cano
from .entidades.chao import Chao
from .configuracao import (IMAGENS, TELA_LARGURA, TELA_ALTURA, FPS,
                           RECOMP_VIVO, RECOMP_PASSAR_CANO, PROB_PULAR, PENALIDADE)

CENARIO = 3
geracao = 0
TELA = IMAGEM_FUNDO = FONTE_PONTOS = None

class JogoEncerrado(Exception):
    """Janela fechada pelo usuário."""


def inicializar(cenario=3):
    global CENARIO, geracao, TELA, IMAGEM_FUNDO, FONTE_PONTOS
    CENARIO = cenario
    geracao = 0
    pygame.init()
    TELA = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption("Flappy Bird - UFRJ")
    IMAGEM_FUNDO = pygame.transform.scale2x(pygame.image.load(str(IMAGENS / "bg_night.png")))
    FONTE_PONTOS = pygame.font.SysFont("arial", 30)


def get_index(canos, passaros):
    # pegando a posição X dos passaros
    passaro_x = passaros[0].x
    # calcule a delta x entre os pássaros e cada cano
    list_distance = [cano.x + cano.LARGURA - passaro_x for cano in canos]
    # pegando o índice do cano que tem a distância mínima não negativa (o cano mais próximo na frente do pássaro)
    index = list_distance.index(min(i for i in list_distance if i >= 0))
    return index


def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_FUNDO, (0, 0))  # desenhando plano de fundo do jogo

    # Desenhando os passaros
    for passaro in passaros:
        passaro.desenhar(tela)

    # Desenhando os canos
    for cano in canos:
        cano.desenhar(tela)

    # Pontuação
    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA-10 - texto.get_width(), 10))

    # Gerações
    texto = FONTE_PONTOS.render(f"Geração: {geracao}", 1, (255, 255, 255))
    tela.blit(texto, (10, 10))
    # Quant. Vivos
    texto = FONTE_PONTOS.render(
        f"Vivos: {len(passaros)}", 1, (255, 255, 255))
    tela.blit(texto, (10, 40))

    # desenhando o chao
    chao.desenhar(tela)

    # atualizando tela
    pygame.display.update()


def flappy_bird(genomas, config):  # fitness function
    global geracao
    tela = TELA
    geracao += 1  # atualizando geração

    # Criando a rede neural
    redes = []  # lista para armazenar todas as redes neurais de treinamento
    lista_genomas = []  # lista para armazenar todos os genomas de treinamento
    passaros = []  # lista para armazenar todos os passaros de treinamento

    for _, genoma in genomas:
        # configurando a rede neural para cada genoma usando a configuração que definimos
        rede = neat.nn.FeedForwardNetwork.create(genoma, config)
        redes.append(rede)  # adicionando a rede neural a lista
        # adicionando o genoma a lista
        lista_genomas.append(genoma)
        genoma.fitness = 0  # iniciando fitness zerada
        # criando passaro e adcionando a lista
        passaros.append(Passaro(230, 350))

    # Instanciando chão e canos
    chao = Chao(730)
    canos = [Cano(700)]

    # pontuação do jogo
    pontos = 0

    # tempo do jogo
    relogio = pygame.time.Clock()

    timestamps = 0
    run = True
    aceleracao = 5
    while run and len(passaros) > 0:

        # verifica os eventos do programa
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                raise JogoEncerrado()

        relogio.tick(FPS)

        # Altera aceleração do jogo
        timestamps += 1

        idx_cano = get_index(canos, passaros)

        # Recompensando cada pássaro com fitness de 0,1 para cada frame que ele permanecer vivo
        for i, passaro in enumerate(passaros):
            # recompensando cada pássaro com fitness de 0,1 para cada frame que ele permanecer vivo
            passaro.mover()
            lista_genomas[i].fitness += RECOMP_VIVO

            # input 1: coordenada vertical do pássaro
            altura_passaro = passaro.y

            # input 2: distância vertical entre o pássaro e o cano superior
            delta_y_top = passaro.y - canos[idx_cano].altura
            # delta_y_top = abs(passaro.y - canos[idx_cano].altura)

            # # input 3: distância vertical entre o pássaro e o tubo inferior
            delta_y_bottom = passaro.y - canos[idx_cano].pos_base
            # delta_y_bottom = abs(passaro.y - canos[idx_cano].pos_base)

            rede_input = (altura_passaro, delta_y_top, delta_y_bottom)
            # enviamos os iputs e obtemos a saída de pular ou não
            output = redes[i].activate(rede_input)

            # A saída da rede é comparada ao limiar configurado para pular.
            if output[0] > PROB_PULAR:
                passaro.pular()

        chao.mover(CENARIO)  # mover o chao

        add_cano = False
        # crie uma lista vazia para conter todos os canos a serem removidos
        remover_canos = []

        for cano in canos:
            # Verifica colisão
            for i in range(len(passaros) - 1, -1, -1):
                passaro = passaros[i]
                # verifique a colisão para cada ave na população
                if cano.colidir(passaro):
                    # aplica a PENALIDADE de colidir com um cano
                    lista_genomas[i].fitness -= PENALIDADE
                    # remove o passaro da lista
                    passaros.pop(i)
                    # remove o genoma do passaro
                    lista_genomas.pop(i)
                    # remove o modelo do passaro da rede
                    redes.pop(i)
                # verifica se o passaro passou corretamente no cano
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    add_cano = True
            cano.mover(CENARIO)  # mover o cano
            # verifica se o cano esta fora da tela para remover
            if cano.x + cano.LARGURA < 0:
                remover_canos.append(cano)

        if add_cano:
            pontos += 1  # adiciona um ponto ao placar
            if CENARIO > 2 and aceleracao <= 10.0:
                # Acelera a passagem do cano pela tela
                aceleracao += 0.01*(timestamps/3)

            new_pipe = Cano(600, aceleracao)
            canos.append(new_pipe)  # cria um novo cano

            # Recompensando os passaros que passam corretamente no cano
            for genoma in lista_genomas:
                genoma.fitness += RECOMP_PASSAR_CANO

        # remove os canos que ja sairam da tela
        for cano in remover_canos:
            canos.remove(cano)

        # verifica colisão do passaro com o teto ou o chão
        for i in range(len(passaros) - 1, -1, -1):
            passaro = passaros[i]
            if (passaro.y + passaro.ALTURA) > chao.y or passaro.y < 0:
                passaros.pop(i)
                lista_genomas.pop(i)
                redes.pop(i)

        # desenha a janela do jogo
        desenhar_tela(tela, passaros, canos, chao, pontos)

