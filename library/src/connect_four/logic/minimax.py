
import math
import random
from functools import partial
from connect_four.logic.models import Checker, GameState, Move

def find_best_move(game_state: GameState) -> Move | None:
    maximizer = game_state.current_checker
    bound_minimax = partial(minimax_scoring, maximizer=maximizer)
    return max(game_state.possible_moves, key=bound_minimax)





def minimax_scoring(
        move:Move, depth: int, alpha: int, beta:int, maximizer: Checker, choose_highest_score: bool = False) -> int:
    if move.after_state.game_over:
        return move.after_state.evaluate_terminal_score(maximizer)
    else:
        if choose_highest_score:
            value = -math.inf
            next_moves =  move.after_state.possible_moves
            selected_move:Move = random.choice(next_moves)
            for move in next_moves:
                col = move.column_index
                state = move.after_state
                new_move = state.make_move_to(col)
                new_score = minimax_scoring(new_move,)




    return value

    ##return (max if choose_highest_score else min)(
       ## minimax(next_move, maximizer, not choose_highest_score)
        ##for next_move in move.after_state.possible_moves
    