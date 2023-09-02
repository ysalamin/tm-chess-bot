def letter_to_cord(coord):
    x = 0
    y = 0

    # Lignes : 1 = 0
    y = int(coord[1]) - 1
    
    # Colonnes : a = 1

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
    depart = ""
    arrivee = ""
    for i in range(0,len(move)):
        if i <= len(move)//2-1:
            depart += move[i]
        else:
            arrivee += move[i]
    d = letter_to_cord(depart)
    a = letter_to_cord(arrivee)
    return d, a

def traduction_piece(piece):
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