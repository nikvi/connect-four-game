
from connect_four_game.game.players import Player
from connect_four_game.logic.exceptions import InvalidMove
from connect_four_game.logic.models import GameState, Move

class ConsolePlayer(Player):
    def get_move(self, game_state: GameState) -> Move | None:
        while not game_state.game_over:
            try:
                column = check_input(input(f"{self.checker.name}'s move: ").strip())
            except ValueError:
                print("Please enter a number from 1 to 7")
            else:
                try:
                    return game_state.make_move_to(column)
                except InvalidMove:
                    print("That column is already full")
        return None
    
def check_input(column: str) -> int:
    position = int(column)
    if  position < 8 and position > 0:
            return (position -1)
    else:
        raise ValueError("Invalid Input")