import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Add this class for Koyeb Health Checks
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_server():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# Start the health server in a background thread
threading.Thread(target=run_health_server, daemon=True).start()

import random

class Board:
    """
    Main board class. Sets board size, number of ships, the player's name
    and the board type (player vs computer).
    """
    def __init__(self, size, num_ships, name, type):
        self.size = size
        self.num_ships = num_ships
        self.name = name
        self.type = type
        self.board = [["." for x in range(size)] for y in range(size)]
        self.ships = []
        self.guesses = []

    def print_board(self):
        """
        Prints the board to the terminal.
        """
        print(f"--- {self.name}'s Board ---")
        for row in self.board:
            print(" ".join(row))
        print("-" * (self.size * 2 + 10))

    def add_ship(self, x, y):
        """
        Adds a ship to the board coordinates.
        """
        if len(self.ships) >= self.num_ships:
            print("Error: Maximum ships reached.")
        else:
            self.ships.append((x, y))
            if self.type == "player":
                self.board[x][y] = "S"

    def guess(self, x, y):
        """
        Processes a guess against the board.
        Returns 'hit', 'miss', or 'already guessed'.
        """
        self.guesses.append((x, y))
        
        if (x, y) in self.ships:
            self.board[x][y] = "X"
            return "hit"
        else:
            self.board[x][y] = "O"
            return "miss"

def get_grid_size():
    """
    Function to get and validate grid size from the user.
    Hides 'Already has info' by setting a default if needed.
    """
    while True:
        try:
            size = input("Enter board size (5-10): \n")
            size = int(size)
            if 5 <= size <= 10:
                return size
            else:
                print("Please choose a number between 5 and 10.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def populate_board(board):
    """
    Randomly places ships on the board.
    """
    while len(board.ships) < board.num_ships:
        x = random.randint(0, board.size - 1)
        y = random.randint(0, board.size - 1)
        if (x, y) not in board.ships:
            board.add_ship(x, y)

def validate_coordinates(size):
    """
    Validates user input for row and column guesses.
    """
    while True:
        try:
            x = int(input(f"Enter Row (0-{size - 1}): \n"))
            y = int(input(f"Enter Column (0-{size - 1}): \n"))
            if 0 <= x < size and 0 <= y < size:
                return x, y
            else:
                print(f"Off-grid! Stay between 0 and {size - 1}.")
        except ValueError:
            print("Invalid input. Please enter numbers only.")

def play_game():
    """
    Main game logic and loop.
    """
    print("Welcome to Battleships!")
    name = input("Enter your name: \n")
    
    size = get_grid_size()
    num_ships = 4 # You can make this dynamic if you want
    
    player_board = Board(size, num_ships, name, type="player")
    computer_board = Board(size, num_ships, "Computer", type="computer")
    
    populate_board(player_board)
    populate_board(computer_board)
    
    while True:
        # Show boards
        player_board.print_board()
        computer_board.print_board() # Computer ships are hidden ('.')
        
        # Player Turn
        print(f"\n{name}'s turn to guess!")
        x, y = validate_coordinates(size)
        
        if (x, y) in computer_board.guesses:
            print("You already guessed that! Try again.")
            continue
            
        result = computer_board.guess(x, y)
        print(f"Result: {result.upper()}!")
        
        # Check Win
        if all(ship in computer_board.guesses for ship in computer_board.ships):
            print(f"CONGRATULATIONS! {name} wins!")
            break
            
        # Computer Turn (Simple AI)
        print("\nComputer is thinking...")
        while True:
            cx = random.randint(0, size - 1)
            cy = random.randint(0, size - 1)
            if (cx, cy) not in player_board.guesses:
                break
        
        c_result = player_board.guess(cx, cy)
        print(f"Computer guessed ({cx}, {cy}): {c_result.upper()}")
        
        # Check Computer Win
        if all(ship in player_board.guesses for ship in player_board.ships):
            print("Game Over. The Computer won.")
            break

if __name__ == "__main__":
    play_game()