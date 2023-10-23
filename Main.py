import random as r
import pygame
import chess
import AI_file
import Translate
import Ouvertures



PROFONDEUR_DE_CALCUL = 2 # Inscrivez ici la difficulté allant de 2 à 4
COULEUR_JOUEUR = True  #True = Blanc
COULEUR_ORDI = not COULEUR_JOUEUR


WIDTH, HEIGHT = 500, 500
TAILLE_CASE = WIDTH/8
PIECE_EN_SELECTION = None
DEPART = None
ARRIVEE = None
COORDONEES_PIECE = None
J_DEJA_ROCK = False
O_DEJA_ROCK = False

opening = Ouvertures.Ouverture_Noire if COULEUR_JOUEUR else Ouvertures.Ouvertures_Blanche
opening = r.choice(opening)



def chess_board():
    global board
    board = chess.Board()
    for ligne in range(8):
        for colonne in range(8):
            square = pygame.Rect(ligne * TAILLE_CASE,
                                 colonne*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            if ((colonne + ligne) % 2) == 0:
                pygame.draw.rect(screen, pygame.Color(230, 230, 230), square)
            else:
                pygame.draw.rect(screen, pygame.Color(55, 55, 55), square)


def chess_pieces():
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
    # Régler un bug de symétrie :

    start_x = start[0]
    start_y = 7-start[1]

    end_x = end[0]
    end_y = end[1]

    # Effacer la pièce du carré ( on dessine un carré par dessus)
    square = pygame.Rect(start_x * TAILLE_CASE, start_y *
                         TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
    pygame.draw.rect(screen, pygame.Color(230, 230, 230) if (
        (start_x + start_y) % 2 == 0) else pygame.Color(55, 55, 55), square)

    # Dessiner la nouvelle piece

    # Bug rencontré : quand on mangeait une pièce, elle était tjr affichée derrière
    square = pygame.Rect(end_x * TAILLE_CASE, (7-end_y) *
                         TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
    pygame.draw.rect(screen, pygame.Color(230, 230, 230) if (
        (end_x + end_y) % 2 == 1) else pygame.Color(55, 55, 55), square)

    piece = board.piece_at(chess.square(int(end_x), int(end_y)))

    piece = Translate.traduction_piece(
        str(piece))  # Avant : Q, après : dame_blanc

    image = pygame.image.load(f"pieces/{piece}.png")
    pygame.transform.scale(image, (TAILLE_CASE, TAILLE_CASE))
    screen.blit(image, (TAILLE_CASE*end_x, TAILLE_CASE*(7-end_y)))


def coup_joueur(coup, depart, arrivee):
    board.push(coup)
    update_board(depart, arrivee)


def coup_ordi(move_counts):
    global J_DEJA_ROCK, O_DEJA_ROCK
    if move_counts < len(opening) and opening[move_counts + 1] != None:
        coup_ordi = opening[move_counts + 1]
        coup_ordi = chess.Move.from_uci(coup_ordi)

    else:
        _, coup_ordi = AI_file.meilleur_coup_alpha_beta(
            board, PROFONDEUR_DE_CALCUL, COULEUR_ORDI)  # Meilleur coup

    board.push(coup_ordi)  # On le bouge dans la logique
    O_DEJA_ROCK = check_rock(coup_ordi, COULEUR_ORDI, O_DEJA_ROCK)
    # On transforme une string"d2d4" en coordonée "4,0"
    t = Translate.split(str(coup_ordi))
    update_board(t[0], t[1])  # On le bouge graphiquement


def green_circle(coordonees):
    '''
    dessines un cercle centré sur les coordonees
    '''
    cercle = pygame.image.load("other_images/circle.png")
    cercle = pygame.transform.scale(cercle, (TAILLE_CASE, TAILLE_CASE))
    screen.blit(
        cercle, (TAILLE_CASE * coordonees[0], TAILLE_CASE*(7-coordonees[1])))


def update():
    pygame.display.update()
    clock.tick(30)


def end_screen(font):
    '''
    affiche un écran de fin
    '''
    text = font.render("Fin de partie !", True, (200, 100, 200))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text, text_rect)
    update()


def manage_promotion(depart, arrivee, coup, couleur):
    # Pour les blancs
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
    if fait:
        return True
    coup = str(coup)
    rock_possibles = ["e1g1", "e8g8", "e1c1", "e8c8"]
    if coup in rock_possibles:
        x_square = None
        y_square = None
        cord_new_rook = None

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
        if x_square/TAILLE_CASE + y_square/TAILLE_CASE % 2 == 0:
            pygame.draw.rect(screen,pygame.Color(230,230,230), square)
        else:
            pygame.draw.rect(screen,pygame.Color(50,50,50), square)

        if couleur:
            couleur = "blanc"
        else:
            couleur = "noir"

        image = pygame.image.load(f"pieces/tour_{couleur}.png")
        pygame.transform.scale(image, (TAILLE_CASE, TAILLE_CASE))
        screen.blit(image, cord_new_rook)

        update()
        return True


def jeu(event):
    global PIECE_EN_SELECTION, DEPART, COORDONEES_PIECE
    global ARRIVEE, J_DEJA_ROCK, O_DEJA_ROCK

    if event.type == pygame.QUIT:
        return False

    if len(board.move_stack) == 0 and not COULEUR_JOUEUR:
        coup_ordi(len(board.move_stack))
        print(coup_ordi)

    elif event.type == pygame.MOUSEBUTTONDOWN:  # Ecouter s'il y a un clic de souris
        if event.button == 1:  # Vérifier que c'est un clic gauche

            # On utilise event.pos[0] pour avoir la coordonée x, et 1 pour y.
            x, y = coordonees_case(event.pos[0], event.pos[1])
            y = 7-y

            # Position de la pièce en module chess format
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

                    J_DEJA_ROCK = check_rock(
                        coup, COULEUR_JOUEUR, J_DEJA_ROCK)
                    if board.is_game_over() is False:
                        update()
                        coup_ordi(len(board.move_stack))

                        PIECE_EN_SELECTION = None
                        DEPART = None
                        ARRIVEE = None
                        COORDONEES_PIECE = None
                    else:
                        PIECE_EN_SELECTION = None
                        DEPART = None
                        ARRIVEE = None
                        COORDONEES_PIECE = None
    return True


def main():
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont("Arial", 80)
    pygame.display.set_caption("Chess board")
    clock = pygame.time.Clock()
    chess_board()
    chess_pieces()
    running = True

    while running:  # Boucle de jeu
        for event in pygame.event.get():  # On ecoute en attente d'input
            running = jeu(event)
            update()
        if board.is_game_over():
            end_screen(font)
            pygame.time.wait(5000)
            running = False
    pygame.quit()


main()
