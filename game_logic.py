class Grid:
    def __init__(self):
        self.size = 5
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]

    def display(self):
        for row in self.board:
            print(' '.join(row))
        print('\n')
    
    def is_within_bounds(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def move_character(self, character, new_row, new_col):
        if not self.is_within_bounds(new_row, new_col):
            return False
        
        cur_row, cur_col = character.position
        if self.board[new_row][new_col] and self.board[new_row][new_col].startswith(character.player):
            return False

        self.board[cur_row][cur_col] = ''
        self.board[new_row][new_col] = f"{character.player}-{character.name}"
        character.set_position(new_row, new_col)

class Character:
    def __init__(self, name, player):
        self.name = name
        self.player = player
        self.position = None
    

    def set_position(self, row, col):
        self.position = (row, col)
    
    def move(self, direction, grid):
        pass

class Pawn(Character):
    def move(self, direction, grid):
        row, col = self.position
        if direction == 'L':
            new_row, new_col = (row, col - 1)
        elif direction == 'R':
            new_row, new_col = (row, col + 1)
        elif direction == 'F':
            new_row, new_col = (row - 1, col) if self.player == 'A' else (row + 1, col)
        elif direction == 'B':
            new_row, new_col = (row + 1, col) if self.player == 'A' else (row - 1, col)
        else:
            return False
        return grid.move_character(self, new_row, new_col)

class Hero1(Character):
    def move(self, direction, grid):
        row, col = self.position
        if direction == 'L':
            new_row, new_col = row, col - 2
        elif direction == 'R':
            new_row, new_col = row, col + 2
        elif direction == 'F':
            new_row, new_col = (row - 2, col) if self.player == 'A' else (row + 2, col)
        elif direction == 'B':
            new_row, new_col = (row + 2, col) if self.player == 'A' else (row - 2, col)
        else:
            return False
        return grid.move_character(self, new_row, new_col)

class Hero2(Character):
    def move(self, direction, grid):
        row, col = self.position
        if direction == 'FL':
            new_row, new_col = (row - 2, col - 2) if self.player == 'A' else (row + 2, col + 2)
        elif direction == 'FR':
            new_row, new_col = (row - 2, col + 2) if self.player == 'A' else (row + 2, col - 2)
        elif direction == 'BL':
            new_row, new_col = (row + 2, col - 2) if self.player == 'A' else (row - 2, col + 2)
        elif direction == 'BR':
            new_row, new_col = (row + 2, col + 2) if self.player == 'A' else (row - 2, col - 2)
        else:
            return False
        return grid.move_character(self, new_row, new_col)

class Game:
    def  __init__(self):
        self.grid = Grid()
        self.current_player = 'A'
        self.players = {'A': [], 'B' : []}
    
    def place_character(self, row, col, character):
        self.grid.board[row][col] = character
        print(f"Placed {character} at ({row}, {col})")
        print("Current board state:", self.grid.board)

    def add_player_characters(self, player, characters):
        self.players[player] = characters
        row = 4 if player == 'A' else 0
        for i, character in enumerate(characters):
            character.set_position(row, i)
            self.grid.board[row][i] = f"{player}-{character.name}"
    
    def switch_turn(self):
        self.current_player = 'B' if self.current_player == 'A' else 'A'
    
    def is_valid_move(self, character, direction):
        if character.player != self.current_player:
            print(f"It's not {character.player}'s turn!")
            return False
        return character.move(direction, self.grid)

    def play_turn(self, character_name, direction):
        for character in self.players[self.current_player]:
            if character.name == character_name:
                if self.is_valid_move(character, direction):
                    self.switch_turn()
                    return True
                else:
                    print("Invalid move, try again!")
                    return False
        print("Character not found.")
        return False

    def display(self):
        self.grid.display()
