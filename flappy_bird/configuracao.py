"""Parâmetros do jogo e caminhos independentes do diretório de execução."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
IMAGENS = RAIZ / "assets" / "imagens"
CONFIG_NEAT = RAIZ / "config" / "neat.ini"
CHECKPOINTS_HISTORICOS = RAIZ / "checkpoints" / "historicos"
CHECKPOINTS_EXECUCOES = RAIZ / "checkpoints" / "execucoes"
RESULTADOS = RAIZ / "resultados" / "execucoes"
TELA_LARGURA = 500
TELA_ALTURA = 800
FPS = 30
MAX_GEN = 50
RECOMP_PASSAR_CANO = 5
RECOMP_VIVO = 0.1
PROB_PULAR = 0.5
PENALIDADE = 1
