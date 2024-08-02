
from __future__ import annotations
import enum
import math
import random
from dataclasses import dataclass
import numpy as np
from functools import cached_property

from connect_four_game.logic.exceptions import InvalidGameState, InvalidMove, UnknownGameScore

ROW_COUNT = 6
COLUMN_COUNT = 7

class Checker(enum.IntEnum):
    YELLOW = 1
    RED = 2

    @property
    def other(self) -> Checker:
        return Checker.YELLOW if self is Checker.RED else Checker.RED


class Board(object):
    
    def __init__(self,board_pos: np.ndarray = None) -> None:
        if board_pos is None:
            self.cells = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=np.uint8)
        else:
            self.cells = board_pos

    def __post_init__(self) -> None:
        if not np.isin(self.board.cells, [0,1,2]).all():
            raise ValueError("Board must only contain 0s, 1s, 2s")
        
    #ensures it only runs once
    @cached_property
    def yellow_count(self) -> int:
        return np.count_nonzero(self.cells == 1)
    
    @cached_property
    def red_count(self) -> int:
        return np.count_nonzero(self.cells == 2)
    
    @cached_property
    def empty_count(self) -> int:
        return np.count_nonzero(self.cells == 0)

@dataclass(frozen=True)
class Move:
    checker: Checker
    row_index: int
    column_index: int
    before_state: GameState
    after_state: GameState

@dataclass(frozen=True)
class GameState:
    board: Board
    starting_checker: Checker = Checker.YELLOW
      
    def validate_game_state(self) -> None:
        if abs(self.board.yellow_count - self.board.red_count) > 1:
            raise InvalidGameState("Wrong number of Red and Yellow checkers")
    
    def validate_starting_mark(self) -> None:
        if self.board.yellow_count > self.board.red_count:
            if self.starting_checker != 1:
                raise InvalidGameState("Wrong starting checker!")
            elif self.board.red_count > self.board.yellow_count:
                if self.starting_checker != 2:
                    raise InvalidGameState("Wrong starting checker")
   
    def validate_winner(self) -> None:
        if self.winner == Checker.YELLOW:
            if self.starting_checker == Checker.YELLOW :
                if self.board.yellow_count <= self.board.red_count:
                    raise InvalidGameState("Wrong number of Yellow checkers")
            else:
                if self.board.yellow_count != self.board.red_count:
                    raise InvalidGameState("Wrong number of Yellow checkers")
        elif self.winner == Checker.RED:
            if self.starting_checker == Checker.RED:
                if self.board.red_count <= self.board.yellow_count:
                    raise InvalidGameState("Wrong number of Red checkers")
                else:
                    if self.board.red_count != self.board.yellow_count:
                        raise InvalidGameState("Wrong number of Red checkers")

    def __post_init__(self) -> None:
        self.validate_game_state
        self.validate_starting_mark
        self.validate_game_state

    @cached_property
    def current_checker(self) -> Checker:
        if self.board.red_count == self.board.yellow_count:
            return self.starting_checker
        else:
            return self.starting_checker.other
    
    @cached_property
    def game_not_started(self) -> bool:
        return self.board.empty_count == 42
    
    @cached_property
    def game_over(self) -> bool:
        return self.winner is not None or self.tie
    
    @cached_property
    def tie(self) -> bool:
        return self.winner is None and self.board.empty_count == 0
    
    @cached_property
    def winner(self) -> Checker | None:
        board = self.board.cells
        current_piece = self.current_checker.value
    
        # checking horizontal position
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if board[r][c] == current_piece and board[r][c+1] == current_piece and board[r][c+2] == current_piece and board[r][c+3] == current_piece:
                    return self.current_checker
                
        # checking vertical position
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == current_piece and board[r+1][c] == current_piece and board[r+2][c] == current_piece and board[r+3][c] == current_piece:
                    return self.current_checker
        
        # checking first diagonal postion
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == current_piece and board[r+1][c+1] == current_piece and board[r+2][c+2] == current_piece and board[r+3][c+3] == current_piece:
                    return self.current_checker
        
        # checking opposite diagonal
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == current_piece and board[r-1][c+1] == current_piece and board[r-2][c+2] == current_piece and board[r-3][c+3] == current_piece:
                    return self.current_checker
        
        return None
    

    def make_move_to(self, col_index: int) -> Move:
        if self.board.empty_count == 0:
            raise InvalidMove("No more moves left")
        row_index = self.find_open_row(col_index)
        new_cells = np.array(self.board.cells)
        new_cells[row_index][col_index] = self.current_checker
        return Move(
            checker=self.current_checker,
            row_index=row_index,
            column_index=col_index,
            before_state=self,
            after_state=GameState(
                Board(new_cells),
                self.starting_checker,
            )
        )
    
    def find_open_row(self, col: int) -> int:
        for r in range(ROW_COUNT):
            if self.board.cells[r][col] == 0:
                return r

    @cached_property
    def possible_moves(self) -> list[Move]:
        moves = []
        if not self.game_over:
            for col in range(COLUMN_COUNT):
                if self.board.cells[ROW_COUNT -1][col] == 0:
                    moves.append(self.make_move_to(col))
        return moves
    
    def make_random_move(self) -> Move | None:
        try:
            return random.choice(self.possible_moves)
        except IndexError:
            return None
    
    def evaluate_block(self, block) -> int:
        score = 0
        current_value = self.current_checker.value
        opposite_value = self.current_checker.other.value
        if block.count(current_value) == 4:
            score += 100
        elif block.count(current_value) == 3 and block.count(0) == 1:
            score += 5
        elif block.count(current_value) == 2 and block.count(0) == 2:
            score += 2
        ## adversial
        if block.count(opposite_value) == 3 and block.count(0) == 1:
            score -= 4
        return score
        
    # scoring heurist - random values
    # need to validate the other good positions nearby
    def score_postion(self) -> int:
        score = 0
        board_pos = self.board.cells
        checker_val = self.current_checker

        #score the board - center
        center_line = [int(i) for i in  list(board_pos[:, COLUMN_COUNT//2])]
        center_count = center_line.count(checker_val)
        score += center_count * 5

        #score vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in  list(board_pos[:, c])]
            for r in range(ROW_COUNT -3):
                block = col_array[r:r+4]
                score += self.evaluate_block(block)

        #score horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board_pos[r,:])]
            for c in range(COLUMN_COUNT-3):
                block = row_array[c:c+4]
                score += self.evaluate_block(block)
                    
        # score diagonal:
        for r in range(ROW_COUNT -3):
            for c in range(COLUMN_COUNT - 3):
                block = [board_pos[r + i][c + i] for i in range(4)]
                score += self.evaluate_block(block)

        #score other diagonal:
        for r in range(ROW_COUNT -3):
            for c in range(COLUMN_COUNT - 3):
                block = [board_pos[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_block(block)
                    
        return score


    
    def evaluate_terminal_score(self, checker: Checker) -> int:
        if self.game_over:
            if self.tie:
                return 0
            # math.inf?
            if self.winner is checker:
                return 9999999
            else:
            # -math.inf ?
                return -9999999
        raise UnknownGameScore("Game is not over yet.")
        

    

            



            
        

        



        


    



