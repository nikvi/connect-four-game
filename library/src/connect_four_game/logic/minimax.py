
import math
import random
from functools import partial
from connect_four_game.logic.models import Checker, GameState, Move

def find_best_move(game_state: GameState) -> Move | None:
    depth = 3
    alpha = -math.inf
    beta = math.inf
    bound_minimax = partial(minimax_scoring,depth=depth, alpha=alpha, beta=beta)
    return max(game_state.possible_moves, key=bound_minimax)

def minimax_scoring(
        move:Move, depth: int, alpha: int, beta:int, choose_highest_score: bool = False) -> int:
    if move.after_state.game_over:
        return move.after_state.evaluate_terminal_score(move.checker)
    elif depth == 0:
        return move.after_state.score_postion()
    else:
        if choose_highest_score:
            value = -9999999
            next_moves =  move.after_state.possible_moves
            #selected_move:Move = random.choice(next_moves)
            for move in next_moves:
                new_score = minimax_scoring(move,depth -1, alpha, beta, False)
                if new_score > value:
                    value = new_score
                    #selected_move = new_move
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
                return value
        else:
            value = 9999999
            next_moves =  move.after_state.possible_moves
            for move in next_moves:
                new_score = minimax_scoring(move,depth -1, alpha, beta, True)
                if new_score < value:
                    value = new_score
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value
    return 0
    ##return (max if choose_highest_score else min)(
       ## minimax(next_move, maximizer, not choose_highest_score)
        ##for next_move in move.after_state.possible_moves
    