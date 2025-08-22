"""
    Fichier principal. Une fois pygame et python-chess téléchargés
    ( à l'aide de pip install pygame et pip install python-chess ),
    il est possible de modifier la Profondeur de calcul du programme pour
    avoir un adversaire difficile (profondeur de 4), moyen ( profondeur 3)
    ou débutant ( profondeur 2 )
"""
# Importations
import random as r
import pygame
import chess
import ai_file
import traductions
import ouvertures

# A modifier
PROFONDEUR_DE_CALCUL = 2 # Inscrivez ici la difficulté allant de 2 à 4
COULEUR_JOUEUR = True #True = Blanc, False = Noir

# Autres constantes
COULEUR_ORDI = not COULEUR_JOUEUR
WIDTH, HEIGHT = 500, 500
TAILLE_CASE = WIDTH/8
PIECE_EN_SELECTION = None
DEPART = None
ARRIVEE = None
COORDONEES_PIECE = None
J_DEJA_ROCK = False
O_DEJA_ROCK = False
opening = ouvertures.Ouverture_Noire if COULEUR_JOUEUR else ouvertures.Ouvertures_Blanche
opening = r.choice(opening)

def chess_board():
    """
    Dessine l'échéquier
    """
    global board
    board = chess.Board()
    for ligne in range(8):
        for colonne in range(8):
            # Création d'un carré, noir ou blanc selon la position
            square = pygame.Rect(ligne * TAILLE_CASE,
                                 colonne*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            if ((colonne + ligne) % 2) == 0:
                pygame.draw.rect(screen, pygame.Color(230, 230, 230), square)
            else:
                pygame.draw.rect(screen, pygame.Color(55, 55, 55), square)

def chess_pieces():
    """
    Affiche les pièces, à partir des images en .png
    La fonction comporte beaucoup de "if" et n'est donc pas très optimisée,
    ce n'est pas si grave étant donné qu'elle ne s'éxecute qu'une seule fois
    """

    # Liste qui faciliteront mes boucles plus tard
    couleur_piece = ["blanc", "noir"]
    type_de_piece = ["pion", "tour", "dame", "roi", "fou", "cavalier"]
    counter_test = 0

    # On load les images et on les mets à la bonne taille
    for couleur in couleur_piece:
        for type in type_de_piece:

            image = pygame.image.load(f"pieces/{type}_{couleur}.png")
            pygame.transform.scale(image, (TAILLE_CASE, TAILLE_CASE))

            # Test pion blanc ( le premier à venir donc counter = 0)
            if counter_test == 0:
                for i in range(8):
                    screen.blit(image, (TAILLE_CASE*i, 6*TAILLE_CASE))

            # Tour
            if counter_test == 1:
                screen.blit(image, (0, 7*TAILLE_CASE))
                screen.blit(image, (7*TAILLE_CASE, 7*TAILLE_CASE))

            # Dame
            if counter_test == 2:
                screen.blit(image, (3*TAILLE_CASE, 7*TAILLE_CASE))

            # Roi
            if counter_test == 3:
                screen.blit(image, (4*TAILLE_CASE, 7*TAILLE_CASE))
            # Fou
            if counter_test == 4:
                screen.blit(image, (2*TAILLE_CASE, 7*TAILLE_CASE))
                screen.blit(image, (5*TAILLE_CASE, 7*TAILLE_CASE))
            # Cavalier
            if counter_test == 5:
                screen.blit(image, (1*TAILLE_CASE, 7*TAILLE_CASE))
                screen.blit(image, (6*TAILLE_CASE, 7*TAILLE_CASE))

            ####### NOIR #######
            # Pion
            if counter_test == 6:
                for i in range(8):
                    screen.blit(image, (TAILLE_CASE*i, 1*TAILLE_CASE))

            # Tour
            if counter_test == 7:
                screen.blit(image, (0*TAILLE_CASE, 0*TAILLE_CASE))
                screen.blit(image, (7*TAILLE_CASE, 0*TAILLE_CASE))

            # Dame
            if counter_test == 8:
                screen.blit(image, (3*TAILLE_CASE, 0*TAILLE_CASE))

            # Roi
            if counter_test == 9:
                screen.blit(image, (4*TAILLE_CASE, 0*TAILLE_CASE))
            # Fou
            if counter_test == 10:
                screen.blit(image, (2*TAILLE_CASE, 0*TAILLE_CASE))
                screen.blit(image, (5*TAILLE_CASE, 0*TAILLE_CASE))
            # Cavalier
            if counter_test == 11:
                screen.blit(image, (1*TAILLE_CASE, 0*TAILLE_CASE))
                screen.blit(image, (6*TAILLE_CASE, 0*TAILLE_CASE))

            counter_test += 1

def coordonees_case(x, y):
    """    Fonction qui convertit une position de souris (par exemple 705x234 pixels) 
    en coordonées 8x8 de case d'échecs
    à l'aide de l'opérateur // qui donne le nombre entier d'une division

    Args:
        x (int): coordonée X en pixel
        y (int): coordonée Y en pixel

    Returns:
        int: coordonées en format de 7x5 par exemple
    """
    return (x//TAILLE_CASE), (y//TAILLE_CASE)

def update_board(start, end):
    """
    Fonction qui, éxécutée après chaque mouvement, mets à jour
    l'échiquier graphique avec la partie logique. 

    Args:
        start (tuple): Coordonées de la pièce avant le mouvement
        end (tuple): Coordonées de la pièce après le mouvement
    """
    start_x = start[0]
    start_y = 7-start[1] # Cette ligne m'a permis de réglé un bug de symmétrie
    end_x = end[0]
    end_y = end[1]

    # Effacer les pièces des cases de départ et d'arrivée en redessinant un carré par-dessus
    square = pygame.Rect(start_x * TAILLE_CASE, start_y *
                         TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
    pygame.draw.rect(screen, pygame.Color(230, 230, 230) if (
        (start_x + start_y) % 2 == 0) else pygame.Color(55, 55, 55), square)

    square = pygame.Rect(end_x * TAILLE_CASE, (7-end_y) *
                         TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
    pygame.draw.rect(screen, pygame.Color(230, 230, 230) if (
        (end_x + end_y) % 2 == 1) else pygame.Color(55, 55, 55), square)

    # Quelle pièce doit-on afficher ?
    piece = board.piece_at(chess.square(int(end_x), int(end_y)))
    piece = traductions.traduction_piece(
        str(piece))  # Avant : Q, après : dame_blanc

    # On affiche la pièce aux bonnes coordonées
    image = pygame.image.load(f"pieces/{piece}.png")
    pygame.transform.scale(image, (TAILLE_CASE, TAILLE_CASE))
    screen.blit(image, (TAILLE_CASE*end_x, TAILLE_CASE*(7-end_y)))

def coup_joueur(coup, depart, arrivee):
    """
    Fonction qui contient les deux étapes d'un coup joué par l'humain :
    L'implémentation du coup dans la logique, et l'update graphique

    Args:
        coup (move): coup qui est joué, selon le format du module chess
        depart (tuple): Coordonées de la pièce avant le mouvement
        arrivee (tuple): Coordonées de la pièce après le mouvement
    """
    board.push(coup)
    update_board(depart, arrivee)

def coup_ordi(move_counts):
    """
    Partie du code qui gère les coups de l'ordi.
    On regarde si on s'adapte à une ouverture présente dans ouvertures.py
    puis on utilise le fichier ai_file pour calculer le meilleur coup, on le joue
    et on update.

    Args:
        move_counts (int): compteur de coups dans la partie
    """
    # Si on est au début de partie, on regarde dans les ouvertures
    global J_DEJA_ROCK, O_DEJA_ROCK
    if move_counts < len(opening) and opening[move_counts + 1] is not None:
        coup_ordi = opening[move_counts + 1]
        coup_ordi = chess.Move.from_uci(coup_ordi)

    # Sinon, on procède à la méthode classique
    else:
        _, coup_ordi = ai_file.meilleur_coup_alpha_beta(
            board, PROFONDEUR_DE_CALCUL, COULEUR_ORDI)  # Meilleur coup

    board.push(coup_ordi)
    O_DEJA_ROCK = check_rock(coup_ordi, COULEUR_ORDI, O_DEJA_ROCK)
    t = traductions.split(str(coup_ordi))
    update_board(t[0], t[1])  # On le bouge graphiquement

def green_circle(coordonees):
    """
    Affiche un cercle vert qui montre la pièce en séléction

    Args:
        coordonees (tuple): coordonées où afficher le cercle vert
    """
    cercle = pygame.image.load("other_images/circle.png")
    cercle = pygame.transform.scale(cercle, (TAILLE_CASE, TAILLE_CASE))
    screen.blit(
        cercle, (TAILLE_CASE * coordonees[0], TAILLE_CASE*(7-coordonees[1])))

def update():
    """
    Update l'interface graphique grâce à l'objet "clock"
    """
    pygame.display.update()
    clock.tick(30)

def end_screen(font):
    """
    Affiche un texte qui informe que la partie est finie

    """
    text = font.render("Fin de partie !", True, (200, 100, 200))
    print(f"dfjsodfjsdoifj {type(font)}")
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text, text_rect)
    update()

def manage_promotion(depart, arrivee, coup, couleur):
    """
    S'occupe de vérifier s'il y a une promotion, et de
    choisir la promotion dame si c'est le cas

    Args:
        depart (tuple): cases de la pièce avant le coup
        arrivee (tuple): cases de la pièce après le coup
        coup (move): coup que l'on vérifie
        couleur (booléen): couleur des pièces que l'on regarde

    Returns:
        coup
    """

    piece = board.piece_at(depart)
    if piece is not None and piece.piece_type == chess.PAWN:
        if couleur is True:

            if 63-arrivee < 8 and piece.color == chess.WHITE:
                coup = chess.Move(depart, arrivee, promotion=chess.QUEEN)
        else:
            if 63-arrivee > 55 and piece.color == chess.BLACK:
                coup = chess.Move(depart, arrivee, promotion=chess.QUEEN)

    return coup

def check_rock(coup, couleur, fait):
    """
    Vérifie s'il y a un rock. Si c'est le cas,
    met à jour l'affichage en conséquence

    Args:
        coup (move): coup à vérifier
        couleur (booléen): couleur du coup
        fait (booléen): un rock a-t-il déjà été fait ?

    Returns:
        booléen: booléen qui informe si le rock a déjà été fait
    """
    # Si le rock a déjà été effectué, on actualise la variable
    if fait:
        return True
    coup = str(coup)
    rock_possibles = ["e1g1", "e8g8", "e1c1", "e8c8"]

    # Si le joueur a les droits de rocker
    if coup in rock_possibles:
        x_square = None
        y_square = None
        cord_new_rook = None

        # On mets à jour l'affichage en conséquence
        if coup == "e1g1":
            cord_new_rook = (5*TAILLE_CASE, 7*TAILLE_CASE)
            x_square = 7 * TAILLE_CASE
            y_square = 7 * TAILLE_CASE
        elif coup == "e8g8":
            cord_new_rook = (5*TAILLE_CASE, 0*TAILLE_CASE)
            x_square = 7 * TAILLE_CASE
            y_square = 0 * TAILLE_CASE
        elif coup == "e1c1":
            cord_new_rook = (3*TAILLE_CASE, 7*TAILLE_CASE)
            x_square = 0 * TAILLE_CASE
            y_square = 7 * TAILLE_CASE
        elif coup == "e8c8":
            cord_new_rook = (3*TAILLE_CASE, 0*TAILLE_CASE)
            x_square = 0 * TAILLE_CASE
            y_square = 0 * TAILLE_CASE

        square = pygame.Rect(x_square, y_square, TAILLE_CASE, TAILLE_CASE)

        if ((x_square + y_square)/TAILLE_CASE) % 2 == 0:
            pygame.draw.rect(screen,pygame.Color(230,230,230), square)
        else:
            pygame.draw.rect(screen,pygame.Color(50,50,50), square)

        if couleur:
            couleur = "blanc"
        else:
            couleur = "noir"

        # On affiche la tour au bon endroit
        image = pygame.image.load(f"pieces/tour_{couleur}.png")
        pygame.transform.scale(image, (TAILLE_CASE, TAILLE_CASE))
        screen.blit(image, cord_new_rook)

        update()
        return True

def jeu(event):
    """Boucle de jeu qui écoute les input du joueur
    et qui s'occupe de la séléctions des pièces

    Args:
        event (event): actions qui proviennent du joueur

    Returns:
        _booléen: indique s'il faut continuer
    """
    global PIECE_EN_SELECTION, DEPART, COORDONEES_PIECE
    global ARRIVEE, J_DEJA_ROCK, O_DEJA_ROCK

    # On regarde si le joueur appuie sur la croix
    if event.type == pygame.QUIT:
        return False
    # Si c'est l'ordi qui joue les blancs, il doit commencer
    if len(board.move_stack) == 0 and not COULEUR_JOUEUR:
        coup_ordi(len(board.move_stack))
        print(coup_ordi)

    elif event.type == pygame.MOUSEBUTTONDOWN:  # Ecouter s'il y a un clic de souris
        if event.button == 1:  # Vérifier que c'est un clic gauche

            # On utilise event.pos[0] pour avoir la coordonée x, et 1 pour y.
            x, y = coordonees_case(event.pos[0], event.pos[1])
            y = 7-y

            # Position de la pièce en format du module chess
            position = int((chess.square(x, y)))
            # Pour savoir si il y a une pièce à la position sélectionnée ( et laqifuelle )
            piece = board.piece_at(position)

            if PIECE_EN_SELECTION is None and piece and piece.color == board.turn and piece.color == COULEUR_JOUEUR:
                # On définit alors qu'une pièce est saisie, et on lui assigne sa position
                PIECE_EN_SELECTION = piece
                # Pour l'update de l'affichage, je stock les cases dont j'ai besoin en mon format
                COORDONEES_PIECE = (x, y)
                green_circle((x, y))
                update()
                DEPART = position
            elif PIECE_EN_SELECTION:  # Deuxième cas : une pièce est saisie
                ARRIVEE = position
                coup = chess.Move(DEPART, ARRIVEE)  # On définit le mouvement
                coup = manage_promotion(DEPART, ARRIVEE, coup, COULEUR_JOUEUR)
                if coup in board.legal_moves:  # On regarde si il est légal
                    coup_joueur(coup, COORDONEES_PIECE, (x, y))
                    # On regarde si c'est un rock
                    J_DEJA_ROCK = check_rock(
                        coup, COULEUR_JOUEUR, J_DEJA_ROCK)
                    if board.is_game_over() is False:
                        update()
                        coup_ordi(len(board.move_stack)) # L'ordi joue après le joueur.

                PIECE_EN_SELECTION = None
                DEPART = None
                ARRIVEE = None
                COORDONEES_PIECE = None

    return True

def main():
    """
    Bloc principal du code, qui appelle toutes les autres fonctions
    """
    global screen, clock

    #Initialisation
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont("Arial", 80)
    pygame.display.set_caption("Chess board")
    clock = pygame.time.Clock()
    chess_board()
    chess_pieces()
    running = True

    # Boucle de jeu
    while running:
        for event in pygame.event.get():
            running = jeu(event) # La boucle de jeu s'effectue
            update() # On update l'interface constamment
        if board.is_game_over(): # Fin de partie -> écran de fin et on quitte tout
            end_screen(font)
            pygame.time.wait(5000)
            running = False
    pygame.quit()

main()
