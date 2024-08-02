
from dataclasses import dataclass
from typing import Callable, TypeAlias

from connect_four.game.players import Player
from connect_four.game.renderers import Renderer
from connect_four.logic.exceptions import InvalidMove
from connect_four.logic.models import GameState, Board, Checker

ErrorHandler: TypeAlias = Callable[[Exception], None]

@dataclass(frozen=True)
class ConnectFour:
    player1 : Player
    player2: Player
    renderer: Renderer
    error_handler: ErrorHandler | None = None
            
    def __post_init__(self):
        if self.player1.checker is self.player2.checker:
            raise ValueError("Players must use different marks")

    def play(self, starting_checker:Checker = Checker.YELLOW) -> None:
        game_state = GameState(Board(), starting_checker)
        if game_state is None:
            print("oop")
        while True:
            self.renderer.render(game_state)
            if game_state.game_over:
                break
            player = self.get_current_player(game_state)
            try:
                game_state = player.make_move(game_state)
            except InvalidMove as ex:
                if self.error_handler:
                    self.error_handler(ex)
    
    def get_current_player(self, gameState: GameState) -> Player:
        if gameState.current_checker is self.player1.checker:
            return self.player1
        else:
            return self.player2
    





