import pygame
from Passaro import Passaro
from Cano import Cano
from Chao import Chao
import pickle
import neat

ia_jogando = True
geracao = 0

TELA_LARGURA = 500
TELA_ALTURA = 800
IMAGEM_FUNDO = pygame.transform.scale2x(pygame.image.load('imgs/bg.png'))

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 30)


def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_FUNDO, (0, 0))

    # Desenhando os passaros
    for passaro in passaros:
        passaro.desenhar(tela)

    # Desenhando os canos
    for cano in canos:
        cano.desenhar(tela)

    # Pontuação
    texto = FONTE_PONTOS.render(f"Pontos: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA-10 - texto.get_width(), 10))

    if ia_jogando:
        # Gerações
        texto = FONTE_PONTOS.render(f"Geração: {geracao}", 1, (255, 255, 255))
        tela.blit(texto, (10, 10))
        # Quant. Vivos
        texto = FONTE_PONTOS.render(
            f"Vivos: {len(passaros)}", 1, (255, 255, 255))
        tela.blit(texto, (10, 40))

    chao.desenhar(tela)
    pygame.display.update()


def main(genomas, config):  # fitness function
    global geracao
    geracao += 1

    # Criando a rede neural
    if ia_jogando:
        redes = []
        lista_genomas = []
        passaros = []
        for _, genoma in genomas:
            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)
            genoma.fitness = 0
            lista_genomas.append(genoma)
            passaros.append(Passaro(230, 350))
    else:
        passaros = [Passaro(230, 350)]

    # Instanciando chão e canos
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption("Flappy Bird - UFRJ")
    pontos = 0

    relogio = pygame.time.Clock()

    run = True
    while run and len(passaros):
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
                pygame.quit()

            if not ia_jogando:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        for passaro in passaros:
                            passaro.pular()

        idx_cano = 0
        if len(passaros) > 0:
            # Verifica se deve usar o primeiro ou o segundo cano
            # Possivel PROBLEMA AQUI!
            if len(canos) > 1 and passaros[0].x > canos[0].x + canos[0].CANO_CIMA.get_width():
                idx_cano = 1
        else:
            run = False
            break

        # Recompensando cada pássaro com fitness de 0,1 para cada frame que ele permanecer vivo
        for i, passaro in enumerate(passaros):
            passaro.mover()
            if ia_jogando:
                lista_genomas[i].fitness += 0.1

                # Envia a localização do pássaro, a localização do cano superior e a localização do cano inferior e determine a partir da rede se deve pular ou não
                output = redes[i].activate((passaro.y, abs(passaro.y - canos[idx_cano].altura),
                                            abs(passaro.y - canos[idx_cano].pos_base)))

                # Usamos uma função de ativação TANH para que o resultado fique entre -1 e 1. se mais de 0,5 então pula
                if output[0] > 0.5:
                    passaro.pular()

        chao.mover()

        add_cano = False
        remover_canos = []

        for cano in canos:
            # Verifica colisão
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                    if ia_jogando:
                        lista_genomas[i].fitness -= 1
                        lista_genomas.pop(i)
                        redes.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    add_cano = True
            cano.mover()
            if cano.x + cano.CANO_CIMA.get_width() < 0:
                remover_canos.append(cano)

        if add_cano:
            pontos += 1
            canos.append(Cano(600))
            # Recompensando a rede por ter passado por um cano
            for genoma in lista_genomas:
                genoma.fitness += 5

        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)
                if ia_jogando:
                    lista_genomas.pop(i)
                    redes.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)

        # # termina e salva o resultado apos pontuação definida
        # if pontos > 20:
        #     pickle.dump(redes[0], open("best.pickle", "wb"))
        #     break


def rodar(caminho_config):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                caminho_config)

    # Crie a população, que é o objeto de nível superior para uma execução NEAT.
    populacao = neat.Population(config)

    # Adicione um relátorio durante o progresso das gerações no terminal.
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())

    if ia_jogando:
        ganhador = populacao.run(main)
        # Melhor individuo ao final das 50 gerações
        print('\nMelhor individuo:\n{!s}'.format(ganhador))
    else:
        main(None, None)


if __name__ == '__main__':
    rodar('config.txt')
