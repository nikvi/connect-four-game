

import os
import numpy as np
import textwrap


from connect_four_game.game.renderers import Renderer
from connect_four_game.logic.models import GameState

XPOS, YPOS = os.get_terminal_size()

class ConsoleRenderer(Renderer):
    def render(self, game_state: GameState) -> None:
        clear_screen()
        if game_state.winner:
             print_solid(game_state.board.cells)
             if game_state.winner == 1:
                 winner = "Yellow: ○"
             else:
                winner = "Red: ●" 
             print(f"{winner} wins \N{party popper}")
        else:
            print_solid(game_state.board.cells)
            if game_state.tie:
                print("No one wins this round \N{neutral face}")

def clear_screen() -> None:
    print("\033c", end="")

# check again
def centred(*lines):
    for line in lines:
        yield line.center(XPOS)

def print_solid(cells: np.ndarray) -> None:
    #board needs to be flipped to print
    flipped_board = np.flip(cells, 0)
    flipped_board = flipped_board.astype(int)

    cells_images = [" ", "○", "●"] 
    print(*centred("\n" * ((YPOS - 5) // 2)))
    print(*centred("  1   2   3   4   5   6   7 "))
    for row in flipped_board:
        print(*centred("+---" *6 + "+---+"))
        print(*centred("| " + " | ".join([cells_images[u] for u in row]) + " |"))
    print(*centred("+---" *6 + "+---+"))
    print(*centred(""))
    print(*centred(""))
    print(*centred(""))
    






        



