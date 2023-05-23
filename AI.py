import chess

# Attribuer une valeur à chaque pièce
valeurs = {"P": 1, "N": 3.05, "B" : 3.33, "R": 5.63, "Q": 9.5, "K": 1000,
           "p": -1, "n": -3.05, "b" : -3.33, "r": -5.63, "q": -9.5, "k": -1000 }

# Faire une fonction d'évaluation de position
def eval_position(pos, couleur):
    '''
    Retourne une valeur correspondant à l'état de l'échéquier ( formule : 10x valeurs des pièces + cases disponibles ou controlées)
    Exemple : eval_position(board, blanc) renverra genre + 10 si les blancs sont mieux
    '''

    valeur_totale = 0
    # Pour chaque case
    for case in range(64):

        # La pièce qui est à cette case
        piece = pos.piece_at(case)
        if piece != None:

            # Cases disponibles au déplacement, utile pour l'évaluation
            cases_disponibles = 0
            for move in pos.legal_moves:
                if move.from_square == case:
                    cases_disponibles += 1
            # Si il est blanc on garde les valeurs de base ( positif pour les blancs ), sinon on inverse
            if couleur =="blanc":
                valeur_totale += valeurs[str(piece)] * 10 + cases_disponibles
                
            else:
               valeur_totale -= valeurs[str(piece)] * 10 + cases_disponibles
               

    valeur_totale = round(valeur_totale)
    return valeur_totale

# Faire une fonction qui joue tout les coups possible et return le meilleur coup
def meilleur_coup(board, profondeur, couleur):
    if profondeur == 0 or board.is_game_over():
        return eval_position(board, couleur)
    
    meilleur_choix = None
    meilleur_valeur = 0

    if couleur == "blanc":
        for move in board.legal_moves:

            position = board.copy() # crée une copie de l'échéquier actuel, sur lequel on va travailler sans déranger notre partie
            position.push(move)

            valeur = meilleur_coup(position, profondeur -1, "noir") # Fonction qui se répète, on va au coup d'après mais pour les noirs cette fois
            
            if valeur > meilleur_valeur:
                meilleur_valeur = valeur
                meilleur_choix = move
        return meilleur_choix
    
    else : 
        for move in board.legal_moves:

            position = board.copy() # crée une copie de l'échéquier actuel, sur lequel on va travailler sans déranger notre partie
            position.push(move)

            valeur = meilleur_coup(position, profondeur -1, "blanc") # Fonction qui se répète, on va au coup d'après mais pour les blanc cette fois
            
            if valeur > meilleur_valeur:
                meilleur_valeur = valeur
                meilleur_choix = move
        return meilleur_choix
        