import chess

# Attribuer une valeur à chaque pièce
valeurs = {"P": 1, "N": 3.05, "B" : 3.33, "R": 5.63, "Q": 9.5, "K": 1000,
           "p": -1, "n": -3.05, "b" : -3.33, "r": -5.63, "q": -9.5, "k": -1000 }

# Faire une fonction d'évaluation de position
def eval_position(pos, couleur):

    valeur_totale = 0
    # Pour chaque case
    for case in range(64):

        # La pièce qui est à cette case
        piece = pos.piece_at(case)
        if piece != None:

            # Si il est blanc on garde les valeurs de base ( positif pour les blancs ), sinon on inverse
            if couleur =="blanc":
                valeur_totale += valeurs[str(piece)]
            else:
               valeur_totale -= valeurs[str(piece)]

    valeur_totale = round(valeur_totale)
    return valeur_totale

# Faire une fonction qui joue tout les coups possible et return le meilleur coup
def meilleur_coup(board, couleur):

    meilleur_choix = None
    meilleur_valeur = None
    for coup in board.legal_moves:

        # On fait le coup, on l'évalue et on l'enlève
        board.push(coup)
        valeur_coup = eval_position(board, couleur)
        board.pop()

        if meilleur_valeur==None or valeur_coup > meilleur_valeur :
            meilleur_valeur = valeur_coup
            meilleur_choix = coup

    return meilleur_choix
