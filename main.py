from __future__ import print_function
from visualize import *
import pygame
from Passaro import Passaro
from Cano import Cano
from Chao import Chao
import pickle
import neat

VIZUALICACAO = True
# configuração da tela do jogo
TELA_LARGURA = 500
TELA_ALTURA = 800
TELA = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
# definindo o titulo da janela
pygame.display.set_caption("Flappy Bird - UFRJ")

# carregando imagem de fundo
IMAGEM_FUNDO = pygame.transform.scale2x(pygame.image.load('imgs/bg_night.png'))
# configurando a fonte do jogo
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 30)

# opção de configuração do jogo
FPS = 30  # velocidade de atualização das imagens
max_score = 20  # pontuação maxima para finalizar o jogo
geracao = 0
# diff_inc = False

# Opções do NEAT
geracao = 0  # começamos na geração 0
MAX_GEN = 50  # numero máximo de gerações
recomp_passar_cano = 5  # recompensa para o idividuo q passou corretamento pelo cano
recomp_vivo = 0.1  # recompensar por permaneser vivo
prob_pular = 0.5  # limiar de probabilidade para o passaro pular
penalidade = 1  # penalidade por colidir com o cano


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


def main(genomas, config):  # fitness function
    global geracao, TELA
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
    while run:

        # verifica os eventos do programa
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
                # pickle.dump(redes[0], open("best.pickle", "wb"))
                pygame.quit()

        # finaliza o jogo quando a pontuação exceder a pontuação máxima
        # finaliza o loop e recomeça quando não nao tem nenhum pássaro
        if pontos >= max_score or len(passaros) == 0:
            run = False
            break

        relogio.tick(FPS)
        
        # Altera aceleração do jogo
        timestamps += 1

        idx_cano = get_index(canos, passaros)

        # idx_cano = 0
        # if len(passaros) > 0:
        #     # Verifica se deve usar o primeiro ou o segundo cano
        #     if len(canos) > 1 and passaros[0].x > canos[0].x + canos[0].LARGURA:
        #         idx_cano = 1
        # else:
        #     run = False
        #     break

        # Recompensando cada pássaro com fitness de 0,1 para cada frame que ele permanecer vivo
        for i, passaro in enumerate(passaros):
            # recompensando cada pássaro com fitness de 0,1 para cada frame que ele permanecer vivo
            passaro.mover()
            lista_genomas[i].fitness += recomp_vivo

            # input 1: distância horizontal entre o pássaro e o cano
            delta_x = passaro.x - canos[idx_cano].x
            # delta_x = passaro.y

            # input 2: distância vertical entre o pássaro e o cano superior
            delta_y_top = passaro.y - canos[idx_cano].altura
            # delta_y_top = abs(passaro.y - canos[idx_cano].altura)

            # # input 3: distância vertical entre o pássaro e o tubo inferior
            delta_y_bottom = passaro.y - canos[idx_cano].pos_base
            # delta_y_bottom = abs(passaro.y - canos[idx_cano].pos_base)

            rede_input = (delta_x, delta_y_top, delta_y_bottom)
            # enviamos os iputs e obtemos a saída de pular ou não
            output = redes[i].activate(rede_input)

            # Usamos uma função de ativação TANH para que o resultado fique entre -1 e 1. se mais de 0,5 então pula
            if output[0] > 0.8:
                passaro.pular()

        chao.mover()  # mover o chao
        # if diff_inc:
        #     chao.acelerar()

        add_cano = False
        # crie uma lista vazia para conter todos os canos a serem removidos
        remover_canos = []

        for cano in canos:
            # Verifica colisão
            for i, passaro in enumerate(passaros):
                # verifique a colisão para cada ave na população
                if cano.colidir(passaro):
                    # aplica a penalidade de colidir com um cano
                    lista_genomas[i].fitness -= penalidade
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
            cano.mover()  # mover o cano
            # verifica se o cano esta fora da tela para remover
            if cano.x + cano.LARGURA < 0:
                remover_canos.append(cano)

        if add_cano:
            pontos += 1  # adiciona um ponto ao placar
            new_pipe = Cano(600)
            
            #Acelera a passagem do cano pela tela
            # if diff_inc:
            #     new_pipe.acelerar(timestamps)
            canos.append(new_pipe)  # cria um novo cano

            # Recompensando os passaros que passam corretamente no cano
            for genoma in lista_genomas:
                genoma.fitness += recomp_passar_cano

        # remove os canos que ja sairam da tela
        for cano in remover_canos:
            canos.remove(cano)

        # verifica colisão do passaro com o teto ou o chão
        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.ALTURA) > chao.y or passaro.y < 0:
                passaros.pop(i)
                lista_genomas.pop(i)
                redes.pop(i)

        # desenha a janela do jogo
        desenhar_tela(tela, passaros, canos, chao, pontos)


def rodar_IA(caminho_config):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                caminho_config)

    # Criando a população de acordo com as configurações que fizemos
    populacao = neat.Population(config)

    # Adicione um relátorio durante o progresso das gerações no terminal.
    populacao.add_reporter(neat.StdOutReporter(True))
    status = neat.StatisticsReporter()
    populacao.add_reporter(status)

    # executando a função fitness (principal), o segundo argumento pode ser o numero de gerações maxima
    populacao.run(main)

    # pegando o genoma mais apto como nosso vencedor
    ganhador = status.best_genome()

    # visualizando os resultados
    if VIZUALICACAO:
        node_names = {-1: 'delta_x', -2: 'delta_y_supeior', -
                        3: 'delta_y_inferior', 0: 'Pular ou Não'}
        draw_net(config, ganhador, True, node_names=node_names)
        plot_stats(status, ylog=False, view=True)
        plot_species(status, view=True)

    # Melhor individuo ao final das 50 gerações
    print('\nMelhor individuo:\n{!s}'.format(ganhador))


rodar_IA('config.txt')
