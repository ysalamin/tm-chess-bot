import pygame

# Variables
WIDTH, HEIGHT = 1280, 720

def initialisation(WIDTH, HEIGHT):
    # Initialisation de l'interface graphique
    pygame.init()
    # Création de la fenêtre avec les dimensions données
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #Titre
    pygame.display.set_caption("Chess board")
    # Création d'un objet qui est utile pour gérer le temps
    clock = pygame.time.Clock()
    #On crée la variable qui start la partie
    running = True

def chess_board():

def chess_pieces():

def main():
    #Boucle de jeu
    initialisation(WIDTH, HEIGHT)
    while running :
        for event in pygame.event.get():
            # Si la croix est cliquée, quitte la boucle -> pygame.quit() sera lu
            if event.type == pygame.QUIT:
                running = False

    #Quitte tout
    pygame.quit()

