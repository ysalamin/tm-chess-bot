import pygame

# Variables
WIDTH, HEIGHT = 1000, 1000

def initialisation(WIDTH, HEIGHT):
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
    #  Je définis l'espace entre les cases, pour dessiner dans les bon espaces. C'est égal à la WIDTH car width = height, sinon j'aurais fais x et y
    ESPACE_ENTRE_CASE = WIDTH / 8

    for ligne in range(8):
        for colonne in range(8):
            # Création du caré, puis on le dessine vite avant que la variable change
            # Paramètres : Le point de départ en x, le point de dpart en y, la largeur en x et en y.
            square = pygame.Rect(ligne * ESPACE_ENTRE_CASE, colonne*ESPACE_ENTRE_CASE, ESPACE_ENTRE_CASE, ESPACE_ENTRE_CASE)
            if
            # Si c'est une cast ou il faut mettre du blanc, on met du blanc. On fait 2 if pour noir et bvlanc
            
            


#def chess_pieces():

def main():
    
    # Initialisation, Création, Préparation et d'autres synonymes...
    initialisation(WIDTH, HEIGHT)
    chess_board()
    running = True

    #Boucle de jeu
    while running :
        for event in pygame.event.get():
            # Si la croix est cliquée, quitte la boucle -> pygame.quit() sera lu
            if event.type == pygame.QUIT:
                running = False

        
        pygame.display.flip()

    #Quitte tout
    pygame.quit()

main()
#Me suis arrêté à la ligne 30