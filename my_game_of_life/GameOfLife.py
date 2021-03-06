from sortedcontainers import SortedList
import time
import os

class GameOfLife():  
  def __init__(self, board_dimensions: tuple, initial_cells: list, generations_limit: int = -1,
    waiting_time: float = 1, first_generation_wait: float = 2):
    """
    Class representing the Game of life. It has generations and board dimensions
    """
    assert board_dimensions[0] > 0 and board_dimensions[1] > 0, \
          'Board dimensions must be positive and greater than 0'

    assert len(initial_cells) > 0, 'The set of initial cells must not be empty'

    self.board_width = board_dimensions[0]
    self.board_height = board_dimensions[1]

    self.generations = []

    self.last_generation = self.create_generation(initial_cells)

    self.generations_limit = generations_limit

    self.waiting_time = waiting_time

    self.first_generation_wait = first_generation_wait

  def start(self):
    generations_count = 0

    while self.generations_limit != generations_count:
      self.print_last_generation_board()

      self.next_step()

      if self.generations_limit == -1 and len(self.last_generation) == 0:
        print("No living cells at generation {0}".format(len(self.generations)))
        break
      elif self.last_generation == self.generations[-1]:
        print("Stabilized at generation {0}".format(len(self.generations)))
        break
      
      time.sleep(self.waiting_time if generations_count > 0 else self.first_generation_wait)

      generations_count += 1
    
    return self.generations
    

  def next_step(self) -> SortedList:
    self.generations.append(self.last_generation)

    next_generation = self.evolve()

    self.last_generation = next_generation

    return self.last_generation

  def evolve(self):
    next_generation = self.create_generation([])

    cells_checked = []

    for cell in self.last_generation:
      cells_to_check = [cell_to_check 
                      for cell_to_check in self.get_cell_and_neighbors(cell) 
                      if cell_to_check not in cells_checked and 
                      (cell_to_check not in self.last_generation or cell_to_check == cell)]

      for cell_to_check in cells_to_check:
        if cell_to_check == cell:
          lives_in_next_generation = self.apply_alive_rules(cell_to_check)
        else:
          lives_in_next_generation = self.apply_death_rules(cell_to_check)
        
        if lives_in_next_generation:
          next_generation.add(cell_to_check)

        cells_checked.append(cell_to_check)
    
    return next_generation
      
  def create_generation(self, cells: list) -> SortedList:
    return SortedList(cells, key=GameOfLife.__sort_cells)

  def get_cell_and_neighbors(self, cell:tuple , remove_itself: bool=False) -> list:
    min_x = cell[0] - 1 if cell[0] - 1 >= 0 else cell[0]
    max_x = cell[0] + 1 if cell[0] + 1 < self.board_width else cell[0]

    min_y = cell[1] - 1 if cell[1] - 1 >= 0 else cell[1]
    max_y = cell[1] + 1 if cell[1] + 1 < self.board_height else cell[1]

    cells_to_check = [(x, y) for x in range(min_x, max_x + 1) for y in range(min_y, max_y + 1)]

    if remove_itself:
      cells_to_check.remove(cell)

    return cells_to_check
  
  def apply_alive_rules(self, cell: tuple) -> bool:
    cell_neighbors = self.get_cell_and_neighbors(cell, True)

    live_neighbors = 0

    for neighbor in cell_neighbors:
      if neighbor in self.last_generation:
        live_neighbors += 1
    
    return live_neighbors >= 2 and live_neighbors <= 3

  def apply_death_rules(self, cell: tuple) -> bool:
    cell_neighbors = self.get_cell_and_neighbors(cell, True)

    live_neighbors = 0

    for neighbor in cell_neighbors:
      if neighbor in self.last_generation:
        live_neighbors += 1
    
    return live_neighbors == 3

  def print_last_generation_board(self):
    self.print_generation_board(self.last_generation)

  def print_generation_board(self, generation):
    board = self.get_generation_board(generation)

    console_board = '\n'.join([' '.join(row) for row in board])
    
    os.system('cls' if os.name == 'nt' else 'clear')

    print(console_board)

  def get_generation_board(self, generation=None):
    if generation is None:
      generation = self.last_generation

    board = [[' ' for col in range(self.board_width)] for row in range(self.board_height)]

    for cell in generation:
      board[cell[1]][cell[0]] = '\u2588'

    return board[::-1]

  def get_all_generations_boards(self):
    boards = [self.get_generation_board(generation) for generation in self.generations]
    
    return boards

  @staticmethod
  def __sort_cells(cell):
    return (-cell[1], cell[0])