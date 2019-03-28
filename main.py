from pprint import pprint

from my_game_of_life.GameOfLife import GameOfLife

game = GameOfLife((5, 5), [(2, 3), (3, 2), (1, 1), (2, 1), (3, 1)])

game.start(4)

for board in game.get_all_generations_boards():
  pprint(board)