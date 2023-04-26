import pygame
import chess
import AI_test
import traduction


# Variables
WIDTH, HEIGHT = 500, 500 # Hauteur et largeur de l'interface
TAILLE_CASE = WIDTH/8 # Chaque case représente un huitième des dimensions vu que c'est un échéquier de 8x8
flip_board = True # J'en ai plus besoin je crois
joueur = "blanc" # Couleur du joueur
ordi = "noir" # Couleur de l'ordi

def initialisation(WIDTH, HEIGHT):
    '''
    
    '''
    global clock
    global screen
    # Initialisation de l'interface graphique
    pygame.init()
    # Création de la fenêtre avec les dimensions données
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    #Titre
    pygame.display.set_caption("Chess board")
    # Création d'un objet qui est utile pour gérer le temps
    clock = pygame.time.Clock()
    #On crée la variable qui start la partie
    
def chess_board():
    global board
    # création de l'objet échéquier du module chess ( cela n'inclut pas l'affichage, je vais devoir tout afficher manuellement)
    board = chess.Board()

    for ligne in range(8):
        for colonne in range(8):
            # Création du caré, puis on le dessine vite avant que la variable change
            # Paramètres : Le point de départ en x, le point de dpart en y, la largeur en x et en y.
            square = pygame.Rect(ligne * TAILLE_CASE, colonne*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)

            # Si c'est une case ou il faut mettre du blanc, on met du blanc. On fait 2 if pour noir et bvlanc
            if ((colonne + ligne) % 2) == 0:
                pygame.draw.rect(screen, pygame.Color(230,230,230), square)
            else : 
                pygame.draw.rect(screen, pygame.Color(55,55,55), square)
            
def chess_pieces():
    '''
    Fonction qui affiche les pièces, stockées dans un dossier dans la même branche TM/pieces/pion_noir

    '''
    # Liste qui faciliteront mes boucles plus tard
    couleur_piece = ["blanc", "noir"]
    type_de_piece = ["pion", "tour", "dame", "roi", "fou", "cavalier"]
    counter_test = 0

    # On load les images et on les mets à la bonne taille
    for couleur in couleur_piece:
        for type in type_de_piece:

            image = pygame.image.load(f"pieces/{type}_{couleur}.png")
            pygame.transform.scale(image, (TAILLE_CASE, TAILLE_CASE))

            # On a fait le commun à toutes les pièces, maintenant on va faire plein de if pour afficher chaque pièce au bon endroit

            # Test pion blanc ( le premier à venir donc counter = 0)
            if counter_test == 0:
                # C'est un pion blanc, alors vu qu'il y a 8 pions, on va les affichés 8 fois à intervalle de taille case
                for i in range(8):
                    screen.blit(image,(TAILLE_CASE*i, 6*TAILLE_CASE))
            
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
                    screen.blit(image,(TAILLE_CASE*i, 1*TAILLE_CASE))
            
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

def coordonees_case(x,y):
    '''
    Fonction qui convertit une position de souris ( genre 705x234 pixels) en coordonées 8x8 de case d'échecs
    à l'aide de l'opérateur // qui donne le nombre entier d'une division
    '''
    return (x//TAILLE_CASE), (y//TAILLE_CASE)




def update_board(start, end):
    '''
    Update le mouvement après affichage
    '''
    # Régler un bug de symétrie :

    start_x = start[0]
    start_y = 7-start[1]

    end_x = end[0]
    end_y = end[1]


    # Effacer la pièce du carré ( on dessine un carré par dessus)
    square = pygame.Rect(start_x * TAILLE_CASE, start_y* TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
    pygame.draw.rect(screen, pygame.Color(230,230,230) if ((start_x + start_y) % 2 ==0) else pygame.Color(55,55,55), square)


    # Dessiner la nouvelle piece

    # Bug rencontré : quand on mangeait une pièce, elle était tjr affichée derrière, car j'avais pas effacer le square de fin
    square = pygame.Rect(end_x * TAILLE_CASE, (7-end_y)* TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
    pygame.draw.rect(screen, pygame.Color(230,230,230) if ((end_x + end_y) % 2 ==1) else pygame.Color(55,55,55), square)

 
    piece = board.piece_at(chess.square(int(end_x), int(end_y)))

    
    piece = traduction.traduction_piece(str(piece)) #  Avant : Q, après : dame_blanc
    
    image = pygame.image.load(f"pieces/{piece}.png")
    pygame.transform.scale(image, (TAILLE_CASE, TAILLE_CASE))
    screen.blit(image, (TAILLE_CASE*end_x, TAILLE_CASE*(7-end_y)))
    


def main():

    # Initialisation, Création, Préparation et d'autres synonymes...
    initialisation(WIDTH, HEIGHT)
    chess_board()
    chess_pieces()
    running = True
    piece_saisie = None
    
    while running : # Boucle de jeu

        for event in pygame.event.get(): # On ecoute en attente d'input

            if event.type == pygame.QUIT: # Si la croix est cliquée, quitte la boucle -> pygame.quit() sera lu
                running = False # Quitte la boucle

            # Mouvement ###########################
            elif event.type == pygame.MOUSEBUTTONDOWN: # Ecouter s'il y a un clic de souris
                if event.button == 1: # Vérifier que c'est un clic gauche
                    x, y = coordonees_case(event.pos[0], event.pos[1]) # On utilise event.pos[0] pour avoir la coordonée x, et 1 pour y.
                    y = 7-y
                    
                    position = int((chess.square(x,y))) # Conversion en coordonée du module chess
                    
                    piece = board.piece_at(position) # Pour savoir si il y a une pièce à la position sélectionnée ( et laquelle )

                    if piece_saisie == None and piece and piece.color == board.turn: # Premier cas : aucune pièce n'est en sélection
                        piece_saisie = position # On définit alors qu'une pièce est saisie, et on lui assigne sa position
                        temp = (x,y) # Pour l'update de l'affichage, je stock les cases dont j'ai besoin en mon format
                    elif piece_saisie: # Deuxième cas : une pièce est saisie
                            arrivee = position # Alors le premier clic était stoquée dans piece saisie, le deuxième position sera l'arr
                            coup = chess.Move(piece_saisie, arrivee) # On définit le mouvement
                            if coup in board.legal_moves: # On regarde si il est légal
                                
                                # Coup Joueur
                                board.push(coup) # On effectue le mouvement   
                                update_board(temp, (x,y)) # Update l'affichage, temp = cases départ en mon format, xy = arrivée
                                
                                # Coup AI
                                coup_ordi = AI_test.meilleur_coup(board,ordi) # Meilleur coup
                                board.push(coup_ordi) # On le bouge dans la logique
                                t = traduction.split(str(coup_ordi)) # On transforme une string"d2d4" en coordonée "4,0"
                                update_board(t[0], t[1] ) # On le bouge graphiquement

                                piece_saisie = None # On réinitialise nos variables
                                #print(board) # Affichage du board en ascii pour s'y retrouver
            #######################################

        pygame.display.update() # Update l'affichage
        clock.tick(30) # Pour gérer le temps, j'en sais pas trop plus
    pygame.quit() # Ferme l'interface
main()