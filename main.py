"""Ponto de entrada do trabalho Flappy Bird com NEAT."""

import argparse


def main():
    from flappy_bird.configuracao import MAX_GEN

    parser = argparse.ArgumentParser(description="Flappy Bird com neuroevolução NEAT")
    parser.add_argument("--cenario", type=int, choices=(1, 2, 3), default=3)
    parser.add_argument(
        "--geracoes",
        type=int,
        default=MAX_GEN,
        help="Máximo de gerações adicionais (padrão: %(default)s)",
    )
    parser.add_argument(
        "--do-zero", action="store_true", help="Iniciar uma nova população"
    )
    parser.add_argument("--sem-graficos", action="store_true")
    parser.add_argument("--checkpoint", help="Caminho de um checkpoint específico")
    args = parser.parse_args()
    if args.geracoes < 1:
        parser.error("--geracoes deve ser maior que zero")
    if args.do_zero and args.checkpoint:
        parser.error("--do-zero e --checkpoint não podem ser usados juntos")
    from flappy_bird.treinamento import rodar_ia

    rodar_ia(
        args.cenario,
        args.geracoes,
        not args.do_zero,
        not args.sem_graficos,
        args.checkpoint,
    )


if __name__ == "__main__":
    main()
