"""Regressão da reorganização, sem janela real nem saídas no repositório."""
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["MPLBACKEND"] = "Agg"

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import neat
import pygame
from flappy_bird import jogo
from flappy_bird.configuracao import CHECKPOINTS_HISTORICOS
from flappy_bird.treinamento import carregar_config
from flappy_bird.visualizacao import plot_stats, plot_species


class IntegracaoTest(unittest.TestCase):
    def tearDown(self):
        pygame.quit()

    def test_cenarios_e_checkpoints(self):
        for cenario in (1, 2, 3):
            for historico in (False, True):
                with self.subTest(cenario=cenario, historico=historico):
                    with redirect_stdout(StringIO()):
                        if historico:
                            populacao = neat.Checkpointer.restore_checkpoint(
                                str(CHECKPOINTS_HISTORICOS / f"{cenario}-neat-checkpoint"))
                        else:
                            populacao = neat.Population(carregar_config())
                        stats = neat.StatisticsReporter()
                        populacao.add_reporter(stats)
                        jogo.inicializar(cenario)
                        frames = 0
                        desenhar = jogo.desenhar_tela

                        def limitar(tela, passaros, canos, chao, pontos):
                            nonlocal frames
                            desenhar(tela, passaros, canos, chao, pontos)
                            frames += 1
                            if frames >= 120:
                                for passaro in passaros:
                                    passaro.y = -1000

                        with patch.object(jogo, "FPS", 0), patch.object(jogo, "desenhar_tela", limitar):
                            melhor = populacao.run(jogo.flappy_bird, 1)
                        self.assertIsNotNone(melhor.fitness)
                        self.assertEqual(len(stats.most_fit_genomes), 1)
                        with TemporaryDirectory() as pasta:
                            destino = Path(pasta)
                            plot_stats(stats, filename=destino / "fitness.png")
                            plot_species(stats, filename=destino / "especies.png")
                            self.assertTrue((destino / "fitness.png").is_file())
                            self.assertTrue((destino / "especies.png").is_file())
                        pygame.quit()

    def test_encerrar_janela(self):
        jogo.inicializar()
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        with self.assertRaises(jogo.JogoEncerrado):
            neat.Population(carregar_config()).run(jogo.flappy_bird, 1)


if __name__ == "__main__":
    unittest.main()
