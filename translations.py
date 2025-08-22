"""
Fonctions de traductions, pour passer d'un format à un autre
"""

def letter_to_cord(coord):
    """
    Fonction qui convertit le format "a8" en  0,8

    Args:
        coord (string): coordonée en format échec classique

    Returns:
        tuple: coordonées en format 0,6 
    """
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
    """sépare un coup "e2e4" en ses cases de départ et d'arrivée

    Args:
        move (move): coup, classe du module chess

    Returns:
        string: cases d'arrivées et de départ
    """
    depart = ""
    arrivee = ""
    for i in range(0,len(move)):
        # Si c'est un caractère de la première moitié, elle indique la case de départ
        if i <= len(move)//2-1:
            depart += move[i]
        # Sinon, case d'arrivée
        else:
            arrivee += move[i]
    d = letter_to_cord(depart)
    a = letter_to_cord(arrivee)
    return d, a

def traduction_piece(piece):
    """
    Traduit les pièces du format chess, pour correspondre au nom de mes images.
    Pas très optimisé mais ne s'éxécute qu'une fois, donc cela n'aura pas d'impact
    significatif sur le temps de calcul

    Args:
        piece (piece): classe du module chess
    Returns:
        string: noms du fichier png de la pièce correspondante
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
