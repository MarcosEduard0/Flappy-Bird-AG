"""Execução do NEAT e persistência de resultados por execução."""
from datetime import datetime
from pathlib import Path
import neat
import pygame
from . import jogo
from .configuracao import (CONFIG_NEAT, CHECKPOINTS_HISTORICOS,
                           CHECKPOINTS_EXECUCOES, RESULTADOS, MAX_GEN)


def carregar_config(caminho=CONFIG_NEAT):
    return neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                       neat.DefaultSpeciesSet, neat.DefaultStagnation, str(caminho))


def rodar_ia(cenario=3, geracoes=MAX_GEN, retomar=True, graficos=True, checkpoint=None):
    config = carregar_config()
    origem = Path(checkpoint).resolve() if checkpoint else CHECKPOINTS_HISTORICOS / f"{cenario}-neat-checkpoint"
    if checkpoint or retomar:
        try:
            populacao = neat.Checkpointer.restore_checkpoint(str(origem))
            # A configuração do checkpoint rege a população retomada.
            config = populacao.config
            print(f"População restaurada de {origem}")
        except FileNotFoundError:
            if checkpoint:
                raise
            print(f"Ainda não existe checkpoint para o cenário {cenario}.")
            populacao = neat.Population(config)
    else:
        populacao = neat.Population(config)

    execucao = f"cenario_{cenario}/" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    pasta_checkpoint = CHECKPOINTS_EXECUCOES / execucao
    pasta_checkpoint.mkdir(parents=True, exist_ok=True)
    populacao.add_reporter(neat.StdOutReporter(True))
    status = neat.StatisticsReporter()
    populacao.add_reporter(status)
    populacao.add_reporter(neat.Checkpointer(4, 5, filename_prefix=str(pasta_checkpoint / "neat-checkpoint-")))
    try:
        jogo.inicializar(cenario)
        jogo.geracao = populacao.generation
        melhor = populacao.run(jogo.flappy_bird, geracoes)
    except jogo.JogoEncerrado:
        print("Execução encerrada ao fechar a janela.")
        return None
    finally:
        pygame.quit()

    if graficos:
        from .visualizacao import draw_net, plot_stats, plot_species
        destino = RESULTADOS / execucao
        destino.mkdir(parents=True, exist_ok=True)
        nomes = {-1: "altura_passaro", -2: "delta_y_superior", -3: "delta_y_inferior", 0: "Pular ou não"}
        from graphviz.backend import ExecutableNotFound
        try:
            draw_net(config, melhor, False, node_names=nomes, filename=destino / "topologia")
        except ExecutableNotFound:
            print("Graphviz (dot) indisponível no PATH; topologia salva apenas como fonte DOT.")
        plot_stats(status, filename=destino / "fitness.png")
        plot_species(status, filename=destino / "especies.png")
        print(f"Gráficos salvos em {destino}")
    print(f"Melhor indivíduo:\n{melhor!s}")
    return melhor
