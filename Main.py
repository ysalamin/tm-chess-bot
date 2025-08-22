"""
    Main file. Once pygame and python-chess are installed
    (using pip install pygame and pip install python-chess),
    you can modify the calculation depth of the program to
    have a hard opponent (depth 4), medium (depth 3)
    or beginner (depth 2)
"""
# Imports
import random as r
import pygame
import chess
import engine
import translations
import openings

# To modify
CALCULATION_DEPTH = 2 # Set the difficulty here from 2 to 4
PLAYER_COLOR = True #True = White, False = Black

# Other constants
COMPUTER_COLOR = not PLAYER_COLOR
WIDTH, HEIGHT = 512, 512
SQUARE_SIZE = WIDTH/8
SELECTED_PIECE = None
START = None
END = None
PIECE_COORDS = None
PLAYER_CASTLED = False
COMPUTER_CASTLED = False
opening = openings.White_Openings if PLAYER_COLOR else openings.Black_Openings
opening = r.choice(opening)

def draw_chess_board():
    """
    Draws the chessboard
    """
    global board
    board = chess.Board()
    for row in range(8):
        for col in range(8):
            # Create a square, black or white depending on position
            square = pygame.Rect(row * SQUARE_SIZE,
                                 col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            if ((col + row) % 2) == 0:
                pygame.draw.rect(screen, pygame.Color(230, 230, 230), square)
            else:
                pygame.draw.rect(screen, pygame.Color(55, 55, 55), square)

def draw_chess_pieces():
    """
    Displays the pieces, from .png images
    The function has many "if" statements and is not very optimized,
    but that's not a big deal since it only runs once
    """

    # Lists to facilitate loops later
    piece_colors = ["blanc", "noir"]
    piece_types = ["pion", "tour", "dame", "roi", "fou", "cavalier"]
    counter_test = 0

    # Load images and set to correct size
    for color in piece_colors:
        for type in piece_types:

            image = pygame.image.load(f"pieces/{type}_{color}.png")
            pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

            # Test white pawn (first to come so counter = 0)
            if counter_test == 0:
                for i in range(8):
                    screen.blit(image, (SQUARE_SIZE*i, 6*SQUARE_SIZE))

            # Rook
            if counter_test == 1:
                screen.blit(image, (0, 7*SQUARE_SIZE))
                screen.blit(image, (7*SQUARE_SIZE, 7*SQUARE_SIZE))

            # Queen
            if counter_test == 2:
                screen.blit(image, (3*SQUARE_SIZE, 7*SQUARE_SIZE))

            # King
            if counter_test == 3:
                screen.blit(image, (4*SQUARE_SIZE, 7*SQUARE_SIZE))
            # Bishop
            if counter_test == 4:
                screen.blit(image, (2*SQUARE_SIZE, 7*SQUARE_SIZE))
                screen.blit(image, (5*SQUARE_SIZE, 7*SQUARE_SIZE))
            # Knight
            if counter_test == 5:
                screen.blit(image, (1*SQUARE_SIZE, 7*SQUARE_SIZE))
                screen.blit(image, (6*SQUARE_SIZE, 7*SQUARE_SIZE))

            ####### BLACK #######
            # Pawn
            if counter_test == 6:
                for i in range(8):
                    screen.blit(image, (SQUARE_SIZE*i, 1*SQUARE_SIZE))

            # Rook
            if counter_test == 7:
                screen.blit(image, (0*SQUARE_SIZE, 0*SQUARE_SIZE))
                screen.blit(image, (7*SQUARE_SIZE, 0*SQUARE_SIZE))

            # Queen
            if counter_test == 8:
                screen.blit(image, (3*SQUARE_SIZE, 0*SQUARE_SIZE))

            # King
            if counter_test == 9:
                screen.blit(image, (4*SQUARE_SIZE, 0*SQUARE_SIZE))
            # Bishop
            if counter_test == 10:
                screen.blit(image, (2*SQUARE_SIZE, 0*SQUARE_SIZE))
                screen.blit(image, (5*SQUARE_SIZE, 0*SQUARE_SIZE))
            # Knight
            if counter_test == 11:
                screen.blit(image, (1*SQUARE_SIZE, 0*SQUARE_SIZE))
                screen.blit(image, (6*SQUARE_SIZE, 0*SQUARE_SIZE))

            counter_test += 1

def square_coords(x, y):
    """    Converts a mouse position (e.g. 705x234 pixels) 
    to 8x8 chessboard coordinates
    using // operator for integer division

    Args:
        x (int): X coordinate in pixels
        y (int): Y coordinate in pixels

    Returns:
        int: coordinates in format like 7x5
    """
    return (x//SQUARE_SIZE), (y//SQUARE_SIZE)

def update_board(start, end):
    """
    Updates the graphical chessboard with the logical board after each move. 

    Args:
        start (tuple): Piece coordinates before the move
        end (tuple): Piece coordinates after the move
    """
    start_x = start[0]
    start_y = 7-start[1] # This line fixed a symmetry bug
    end_x = end[0]
    end_y = end[1]

    # Erase pieces from start and end squares by redrawing a square over them
    square = pygame.Rect(start_x * SQUARE_SIZE, start_y *
                         SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(screen, pygame.Color(230, 230, 230) if (
        (start_x + start_y) % 2 == 0) else pygame.Color(55, 55, 55), square)

    square = pygame.Rect(end_x * SQUARE_SIZE, (7-end_y) *
                         SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(screen, pygame.Color(230, 230, 230) if (
        (end_x + end_y) % 2 == 1) else pygame.Color(55, 55, 55), square)

    # Which piece should be displayed?
    piece = board.piece_at(chess.square(int(end_x), int(end_y)))
    piece = translations.translate_piece(
        str(piece))  # Before: Q, after: queen_white

    # Display the piece at the correct coordinates
    image = pygame.image.load(f"pieces/{piece}.png")
    pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
    screen.blit(image, (SQUARE_SIZE*end_x, SQUARE_SIZE*(7-end_y)))

def player_move(move, start, end):
    """
    Contains the two steps of a move played by the human:
    The implementation of the move in logic, and the graphical update

    Args:
        move (move): move played, according to chess module format
        start (tuple): Piece coordinates before the move
        end (tuple): Piece coordinates after the move
    """
    board.push(move)
    update_board(start, end)

def computer_move(move_count):
    """
    Handles computer moves.
    Checks if an opening from openings.py applies,
    then uses ai_file to calculate the best move, plays it,
    and updates.

    Args:
        move_count (int): move counter in the game
    """
    # If at the start of the game, check openings
    global PLAYER_CASTLED, COMPUTER_CASTLED
    if move_count < len(opening) and opening[move_count + 1] is not None:
        computer_move = opening[move_count + 1]
        computer_move = chess.Move.from_uci(computer_move)

    # Otherwise, proceed with classic method
    else:
        _, computer_move = engine.best_move_alpha_beta(
            board, CALCULATION_DEPTH, COMPUTER_COLOR)  # Best move

    board.push(computer_move)
    COMPUTER_CASTLED = check_castle(computer_move, COMPUTER_COLOR, COMPUTER_CASTLED)
    t = translations.split(str(computer_move))
    update_board(t[0], t[1])  # Move graphically

def green_circle(coords):
    """
    Displays a green circle showing the selected piece

    Args:
        coords (tuple): coordinates to display the green circle
    """
    circle = pygame.image.load("other_images/circle.png")
    circle = pygame.transform.scale(circle, (SQUARE_SIZE, SQUARE_SIZE))
    screen.blit(
        circle, (SQUARE_SIZE * coords[0], SQUARE_SIZE*(7-coords[1])))

def update():
    """
    Updates the graphical interface using the "clock" object
    """
    pygame.display.update()
    clock.tick(30)

def end_screen(font):
    """
    Displays text informing that the game is over

    """
    text = font.render("Game Over!", True, (200, 100, 200))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text, text_rect)
    update()

def handle_promotion(start, end, move, color):
    """
    Checks for promotion, and chooses queen promotion if so

    Args:
        start (tuple): piece square before the move
        end (tuple): piece square after the move
        move (move): move to check
        color (bool): color of the pieces to check

    Returns:
        move
    """

    piece = board.piece_at(start)
    if piece is not None and piece.piece_type == chess.PAWN:
        if color is True:

            if 63-end < 8 and piece.color == chess.WHITE:
                move = chess.Move(start, end, promotion=chess.QUEEN)
        else:
            if 63-end > 55 and piece.color == chess.BLACK:
                move = chess.Move(start, end, promotion=chess.QUEEN)

    return move

def check_castle(move, color, done):
    """
    Checks for castling. If so,
    updates the display accordingly

    Args:
        move (move): move to check
        color (bool): color of the move
        done (bool): has castling already been done?

    Returns:
        bool: informs if castling has already been done
    """
    # If castling already done, update variable
    if done:
        return True
    move = str(move)
    possible_castles = ["e1g1", "e8g8", "e1c1", "e8c8"]

    # If player has castling rights
    if move in possible_castles:
        x_square = None
        y_square = None
        new_rook_coords = None

        # Update display accordingly
        if move == "e1g1":
            new_rook_coords = (5*SQUARE_SIZE, 7*SQUARE_SIZE)
            x_square = 7 * SQUARE_SIZE
            y_square = 7 * SQUARE_SIZE
        elif move == "e8g8":
            new_rook_coords = (5*SQUARE_SIZE, 0*SQUARE_SIZE)
            x_square = 7 * SQUARE_SIZE
            y_square = 0 * SQUARE_SIZE
        elif move == "e1c1":
            new_rook_coords = (3*SQUARE_SIZE, 7*SQUARE_SIZE)
            x_square = 0 * SQUARE_SIZE
            y_square = 7 * SQUARE_SIZE
        elif move == "e8c8":
            new_rook_coords = (3*SQUARE_SIZE, 0*SQUARE_SIZE)
            x_square = 0 * SQUARE_SIZE
            y_square = 0 * SQUARE_SIZE

        square = pygame.Rect(x_square, y_square, SQUARE_SIZE, SQUARE_SIZE)

        if ((x_square + y_square)/SQUARE_SIZE) % 2 == 0:
            pygame.draw.rect(screen,pygame.Color(230,230,230), square)
        else:
            pygame.draw.rect(screen,pygame.Color(50,50,50), square)

        if color:
            color_str = "white"
        else:
            color_str = "black"

        # Display rook at correct location
        image = pygame.image.load(f"pieces/rook_{color_str}.png")
        pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
        screen.blit(image, new_rook_coords)

        update()
        return True

def game_loop(event):
    """Game loop that listens to player input
    and handles piece selection

    Args:
        event (event): actions from the player

    Returns:
        _bool: indicates whether to continue
    """
    global SELECTED_PIECE, START, PIECE_COORDS
    global END, PLAYER_CASTLED, COMPUTER_CASTLED

    # Check if player clicks the close button
    if event.type == pygame.QUIT:
        return False
    # If computer plays white, it must start
    if len(board.move_stack) == 0 and not PLAYER_COLOR:
        computer_move(len(board.move_stack))
        print(computer_move)

    elif event.type == pygame.MOUSEBUTTONDOWN:  # Listen for mouse click
        if event.button == 1:  # Check for left click

            # Use event.pos[0] for x coordinate, 1 for y.
            x, y = square_coords(event.pos[0], event.pos[1])
            y = 7-y

            # Piece position in chess module format
            position = int((chess.square(x, y)))
            # Check if there is a piece at the selected position (and which one)
            piece = board.piece_at(position)

            if SELECTED_PIECE is None and piece and piece.color == board.turn and piece.color == PLAYER_COLOR:
                # Define that a piece is picked, and assign its position
                SELECTED_PIECE = piece
                # For display update, store needed squares in my format
                PIECE_COORDS = (x, y)
                green_circle((x, y))
                update()
                START = position
            elif SELECTED_PIECE:  # Second case: a piece is picked
                END = position
                move = chess.Move(START, END)  # Define the move
                move = handle_promotion(START, END, move, PLAYER_COLOR)
                if move in board.legal_moves:  # Check if legal
                    player_move(move, PIECE_COORDS, (x, y))
                    # Check for castling
                    PLAYER_CASTLED = check_castle(
                        move, PLAYER_COLOR, PLAYER_CASTLED)
                    if board.is_game_over() is False:
                        update()
                        computer_move(len(board.move_stack)) # Computer plays after player.

                SELECTED_PIECE = None
                START = None
                END = None
                PIECE_COORDS = None

    return True

def main():
    """
    Main code block, calls all other functions
    """
    global screen, clock

    #Initialization
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont("Arial", 80)
    pygame.display.set_caption("Chess board")
    clock = pygame.time.Clock()
    draw_chess_board()
    draw_chess_pieces()
    running = True

    # Game loop
    while running:
        for event in pygame.event.get():
            running = game_loop(event) # Game loop runs
            update() # Constantly update interface
        if board.is_game_over(): # End of game -> end screen and quit
            end_screen(font)
            pygame.time.wait(5000)
            running = False
    pygame.quit()

main()
