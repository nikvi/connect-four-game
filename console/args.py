
import argparse

from connect_four_game.game.players import  Player, RandomBotPlayer, MinimaxBotPlayer
from connect_four_game.logic.models import Checker

from .players import ConsolePlayer

PLAYER_CLASSES = {
    "human": ConsolePlayer,
    "random": RandomBotPlayer,
    "minimax": MinimaxBotPlayer
}

def parse_args() -> tuple[Player, Player, Checker]:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-Y",
        dest="player_yellow",
        choices=PLAYER_CLASSES.keys(),
        default="human",
    )
    parser.add_argument(
        "-R",
        dest="player_red",
        choices=PLAYER_CLASSES.keys(),
        default="random",
    )
    parser.add_argument(
        "--starting",
        dest="starting_checker",
        choices=Checker,
        type=Checker,
        default=Checker.YELLOW,
    )
    args = parser.parse_args()

    player1 = PLAYER_CLASSES[args.player_yellow](Checker.YELLOW)
    player2 = PLAYER_CLASSES[args.player_red](Checker.RED)

    if args.starting_checker == 2:
        player1, player2 = player2, player1
    
    return player1, player2, args.starting_checker
