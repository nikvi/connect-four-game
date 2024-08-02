
import abc
import time

from connect_four.logic.exceptions import InvalidMove
from tic_tac_toe.logic.minimax import find_best_move
from connect_four.logic.models import Checker, GameState, Move

class Player(metaclass=abc.ABCMeta):
    def __init__(self, checker: Checker) -> None:
        self.checker = checker

    def make_move(self, game_state: GameState) -> GameState:
        if self.checker is game_state.current_checker:
            if move := self.get_move(game_state):
                return move.after_state
            raise InvalidMove("No more possible moves")
        else:
            raise InvalidMove("It's the other player's turn.")
    
    @abc.abstractmethod
    def get_move(self, game_state: GameState) -> Move | None:
        """Raise the current player's move in the given game state."""

class BotPlayer(Player, metaclass=abc.ABCMeta):
    def __init__(self, checker: Checker, delay_seconds: float = 0.25) -> None:
        super().__init__(checker)
        self.delay_seconds = delay_seconds
    
    def get_move(self, game_state: GameState) -> Move | None:
        time.sleep(self.delay_seconds)
        return self.get_bot_move(game_state)
    
    @abc.abstractmethod
    def get_bot_move(self, game_state: GameState) -> Move | None:
        """Return the computer's move in the given game state."""

class RandomBotPlayer(BotPlayer):
    def get_bot_move(self, game_state: GameState) -> Move | None :
        return game_state.make_random_move()

class MinimaxBotPlayer(BotPlayer):
    def get_bot_move(self, game_state: GameState) -> Move | None:
        if game_state.game_not_started:
            return game_state.make_random_move()
        else:
            return find_best_move(game_state)
        

    
