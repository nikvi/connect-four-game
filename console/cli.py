from connect_four.game.engine import ConnectFour

from .args import parse_args
from .renderers import ConsoleRenderer

def main() -> None:
    player1, player2, starting_checker = parse_args()
    ConnectFour(player1, player2, ConsoleRenderer()).play(starting_checker)