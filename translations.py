"""
Translation functions, to convert from one format to another
"""

def letter_to_cord(coord):
    """
    Function that converts the format "a8" to  0,8

    Args:
        coord (string): coordinate in classic chess format

    Returns:
        tuple: coordinates in format 0,6 
    """
    x = 0
    y = 0

    # Rows: 1 = 0
    y = int(coord[1]) - 1
    # Columns: a = 1

    if coord[0] == "a":
        x = 0
    if coord[0] == "b":
        x = 1
    if coord[0] == "c":
        x = 2
    if coord[0] == "d":
        x = 3
    if coord[0] == "e":
        x = 4
    if coord[0] == "f":
        x = 5
    if coord[0] == "g":
        x = 6
    if coord[0] == "h":
        x = 7

    tuple = (x,y)
    return tuple

def split(move):
    """Splits a move "e2e4" into its start and end squares

    Args:
        move (move): move, chess module class

    Returns:
        string: start and end squares
    """
    start = ""
    end = ""
    for i in range(0,len(move)):
        # If it's a character from the first half, it indicates the start square
        if i <= len(move)//2-1:
            start += move[i]
        # Otherwise, end square
        else:
            end += move[i]
    d = letter_to_cord(start)
    a = letter_to_cord(end)
    return d, a

def translate_piece(piece):
    """
    Translates pieces from chess format to match my image names.
    Not very optimized but only runs once, so it won't have a significant impact
    on calculation time

    Args:
        piece (piece): chess module class
    Returns:
        string: png filename of the corresponding piece
    """
    if piece == "q":
        return "dame_noir"
    elif piece == "r":
        return "tour_noir"
    elif piece == "n":
        return "cavalier_noir"
    elif piece == "b":
        return "fou_noir"
    elif piece  == "k":
        return "roi_noir"
    elif piece  == "p":
        return "pion_noir"
    elif piece  == "Q":
        return "dame_blanc"
    elif piece  == "R":
        return "tour_blanc"
    elif piece == "N":
        return "cavalier_blanc"
    elif piece  == "B":
        return "fou_blanc"
    elif piece  == "K":
        return "roi_blanc"
    elif piece  == "P":
        return "pion_blanc"
