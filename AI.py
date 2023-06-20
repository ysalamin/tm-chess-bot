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

        # On regarde s'il y a une pièce
        
        piece = pos.piece_at(case)
        if piece != None:

            # On regarde combien de move il y a de possible. Plus il y a de move possible plus elle est bien positionnée
            move_dispo = 0
            for move in pos.legal_moves:
                if move.from_square == case:
                 move_dispo += 1

            # On ajoute à la valeur de la position la pièce*10 + le nombre de move dispo ( formule arbitraire mais tt se joue la dessus)
            if couleur =="blanc":
                valeur_totale += valeurs[str(piece)] * 10 + move_dispo
                
            else: # dans le cas ou la personne joue les noir, on inverse la valeur. Peu importe sa couleur + = mieux
               valeur_totale -= valeurs[str(piece)] * 10 + move_dispo
               

    valeur_totale = round(valeur_totale)
    return valeur_totale

# Faire une fonction qui joue tout les coups possible et return le meilleur coup
def meilleur_coup(board, profondeur, couleur):
    if profondeur == 0 or board.is_game_over():
        return eval_position(board, couleur)
    
    meilleur_choix = None
    meilleur_valeur = -1000

    if couleur == "blanc":
        for move in board.legal_moves: # Pour toutes les branches hautes de l'arbre

            board_temp = board.copy() # crée une copie de l'échéquier actuel, sur lequel on va travailler sans déranger notre partie
            board_temp.push(move)

            # On plonge dans l'arbre en utilisant la même fonction, qui une fois atteint la profondeur retourne la valeur de la dernière branche
            best_move = meilleur_coup(board_temp, profondeur -1, "noir") # Fonction qui se répète, on va au coup d'après mais pour les noirs cette fois
            # Pour la ligne du dessus, on met " noir " car on veut voir les coups adverses 
            valeur = eval_position(board_temp, couleur) ## PB, faut que je lance avec le board et pas best move
            # / ! \ me faut dont le board du best_move. j'essaie de mettre board_temp comme arg

            if valeur == None:
                valeur = -1000

            if valeur > meilleur_valeur: # On s'actualise sur la meilleure valeure
                meilleur_valeur = valeur
                meilleur_choix = move
        return meilleur_choix
    
    else : 
        for move in board.legal_moves:

            board_temp = board.copy() # crée une copie de l'échéquier actuel, sur lequel on va travailler sans déranger notre partie
            board_temp.push(move)

            best_move = meilleur_coup(board_temp, profondeur -1, "blanc") # Fonction qui se répète, on va au coup d'après mais pour les blanc cette fois
            # On met blanc car là on est noir, et la prochaine branche sera toujours la couleur inverse
            valeur = eval_position(board_temp, couleur)
            if valeur == None:
                valeur = -1000

            if valeur > meilleur_valeur:
                meilleur_valeur = valeur
                meilleur_choix = move
        return meilleur_choix
        