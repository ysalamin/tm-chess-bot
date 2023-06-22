import chess

# Attribuer une valeur à chaque pièce
valeurs = {"P": 1, "N": 3.05, "B" : 3.33, "R": 5.63, "Q": 9.5, "K": 1000,
           "p": -1, "n": -3.05, "b" : -3.33, "r": -5.63, "q": -9.5, "k": -1000 }

# Faire une fonction d'évaluation de position
def eval_position(pos, couleur):

    valeur_totale = 0
    for case in range(64):
        
        piece = pos.piece_at(case)
        if piece != None: # S'il y en a une

            
            move_dispo = 0
            for move in pos.legal_moves:
                if move.from_square == case:
                 move_dispo += 1

            if couleur =="blanc":
                valeur_totale += valeurs[str(piece)] * 10 + move_dispo

            else: 
               valeur_totale -= valeurs[str(piece)] * 10 + move_dispo
               

    valeur_totale = round(valeur_totale)
    return valeur_totale

# Faire une fonction qui joue tout les coups possible et return le meilleur coup
def meilleur_coup(board, profondeur, couleur):
    if profondeur == 0 or board.is_game_over():
        return eval_position(board, couleur)
    
    meilleur_choix = None
    meilleur_valeur = -1000

    couleur_coup_adverse = "noir" if couleur =="blanc" else"blanc"
    for move in board.legal_moves: 

        board_temp = board.copy()
        board_temp.push(move)
  
        
        valeur_au_bout = meilleur_coup(board_temp, profondeur -1, couleur_coup_adverse) # Pas nécéssairement le meilleur
        print(f"voici valeur au bout : {valeur_au_bout}")
        if valeur_au_bout == None:
            valeur_au_bout = -1000

        if valeur_au_bout > meilleur_valeur: # On s'actualise sur la meilleure valeure
            meilleur_valeur = valeur_au_bout
            meilleur_choix = move
        return meilleur_choix
    