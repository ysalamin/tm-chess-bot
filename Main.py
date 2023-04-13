import pygame


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
    à l'aide de l'opérateur // qui donne le nombre entier d'une division, exemple si il y a un échéquier de 800x800:
    je clique sur la case b2 en 150x150, en faisant x//taille_case j'obtiendrais 1. Or je veux obtenir 2, car b2
    est à la 2ème ligne / colonne, donc x//taillecase + 1
    '''
    return (x//TAILLE_CASE + 1), (y//TAILLE_CASE + 1)

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

        
        pygame.display.update()
        clock.tick(30)

    #Quitte tout
    pygame.quit()

main()