"""
    Part of the code that handles the AI
"""
import chess

# Assign a value to each piece
values = {"P": 1, "N": 3.05, "B" : 3.33, "R": 5.63, "Q": 9.5, "K": 1000}

# Evaluation function for board position
def eval_position(pos):
    """
    Evaluates a chessboard by assigning it a value

    Args:
        pos (board): position

    Returns:
        float: value associated with the position
    """

    # Variables
    total_value = 0
    material_value = 0
    tactical_value = 0

    # This block forces the computer to act differently if there is checkmate
    if pos.is_checkmate():
        if pos.turn:
            total_value = -10000
            return total_value
        else:
            total_value = 10000
            return total_value

    # Material value
    for square in range(64):
        piece = pos.piece_at(square)
        if piece is not None:
            piece_value = values[str(piece).upper()]

            # Add to material_value the value of each piece, depending on its color
            material_value += piece_value if (piece.color == chess.WHITE) else -piece_value

    # Tactical value
    possible_moves = pos.legal_moves
    # For each possible move with this piece, add 1 to tactical value
    for move in possible_moves:
        piece = pos.piece_at(move.from_square)
        if piece is not None:
            tactical_value += 1 if (piece.color == chess.WHITE) else -1

    total_value = material_value + tactical_value * 0.1

    return total_value


def best_move_alpha_beta(board, depth, color, alpha=-float("inf"), beta=float("inf")):
    """
    Function that uses the minmax algorithm and alpha-beta pruning
    to calculate all unpruned positions to a depth of X.

    Args:
        board (board): position
        depth (int): calculation depth / number of times recursion
        will occur
        color (bool): color to play
        alpha (float, optional): number, always trying to grow and starting at -infinity
        beta (float, optional): number, always trying to shrink, starting at +infinity

    Returns:
        float: best value
        move: best move, which corresponds to the best value
    """

    if depth == 0 or board.is_game_over():
        return eval_position(board), None

    # Initialization
    best_choice = None

    # If it's white's turn
    if color is True:
        best_value = -float("inf")
        # Perform each possible move on a copy of the board
        for move in board.legal_moves:
            board_temp = board.copy()
            board_temp.push(move)
            # Continue exploring further by recursively calling this function
            value_at_end, _ = best_move_alpha_beta(board_temp, depth -1, False, alpha, beta)

            # Update the best value and the move that goes with it
            if value_at_end > best_value:
                best_value = value_at_end
                best_choice = move

            # Alpha-beta pruning, which allows ignoring part of the tree under condition
            # This is detailed in the documentation and will be explained orally
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break

    # If it's black's turn. Similar except for a few signs
    else:
        best_value = float("inf")
        for move in board.legal_moves:
            board_temp = board.copy()
            board_temp.push(move)
            value_at_end, _ = best_move_alpha_beta(board_temp, depth -1, True, alpha, beta)
            if value_at_end < best_value:
                best_value = value_at_end
                best_choice = move
            beta = min(beta, best_value) # Save the worst move for white in beta
            if beta <= alpha :
                break

    return best_value, best_choice
