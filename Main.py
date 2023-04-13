import pygame
import chess


# Variables
WIDTH, HEIGHT = 500, 500
TAILLE_CASE = WIDTH/8

def initialisation(WIDTH, HEIGHT):
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

def main():
    
    # Initialisation, Création, Préparation et d'autres synonymes...
    initialisation(WIDTH, HEIGHT)
    chess_board()
    chess_pieces()
    running = True

    #Boucle de jeu
    while running :
        
        for event in pygame.event.get():

            # Si la croix est cliquée, quitte la boucle -> pygame.quit() sera lu
            if event.type == pygame.QUIT:
                running = False

            # Ecouter si il y a un clic de souris
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifier que ce soit un clic gauche
                if event.button == 1:
                    # on utilise event.pos[0] pour avoir la coordonée x, et 1 pour y.
                    # on les mets dans ma fonction qui transforme en case d'échéquier pour avoir les cases
                    x, y = coordonees_case(event.pos[0], event.pos[1])
                    print(event.pos[0], event.pos[1], x, y)

                    # Maintenant on veut convertir MON format de coordonée à celui du module chess, en utilisant chess.square
                    # Le format du module est le suivant : en haut à gauche c'est 1, et en bas à droite 64
                    # position est donc la position de la pièce utilisable par le module chess
                    position = int(chess.square(x,y))
                    print(position)

                    # Pour savoir la pièce qu'il y a à cette position : 
                    piece = board.piece_at(position)
                    print(piece)

                    # Si c'est au tour des blancs et qu'une pièce blanche est sélectionnée, on va rentrer dans le mouvement
                    # Donc y'a deux conditions à chequer :
                    # Je note juste que chess.Color() retourne true si la pièce est blanche et board.turn() returne true aussi si
                    # c'est au tour de jouer
                    # Piece vaut None si aucune pièce n'est sélectionnée
                    if piece:
                        if piece.color == board.turn:
                            # On attend la case ou le gars veut la bouger
                            # Ici !




        
        pygame.display.update()
        clock.tick(30)

    #Quitte tout
    pygame.quit()

main()