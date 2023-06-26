import chess

# Attribuer une valeur à chaque pièce
valeurs = {"P": 1, "N": 3.05, "B" : 3.33, "R": 5.63, "Q": 9.5, "K": 1000}

# Faire une fonction d'évaluation de position
def eval_position(pos):

    valeur_totale = 0
    valeur_matérielle = 0
    valeur_tactique = 0

    # Valeur matérielle
    for case in range(64):
        piece = pos.piece_at(case)

        if piece is not None:
            piece_value = valeurs[str(piece).upper()]
    
            valeur_matérielle += piece_value if (piece.color == chess.WHITE) else -piece_value

    # Valeur tactique
    moves_possibles = pos.legal_moves
    for move in moves_possibles:
        piece = pos.piece_at(move.from_square)
        if piece is not None:
            valeur_tactique += 1 if (piece.color == chess.WHITE) else -1

               

    valeur_totale = valeur_matérielle + valeur_tactique * 0.1
    return valeur_totale

# Faire une fonction qui joue tout les coups possible et return le meilleur coup
def meilleur_coup_sans_elagage(board, profondeur, couleur):
    if profondeur == 0 or board.is_game_over():
        return eval_position(board), None
    
    meilleur_choix = None
    meilleur_valeur = -float("inf") if couleur == "blanc" else float("inf")

    for move in board.legal_moves: 

        board_temp = board.copy()
        board_temp.push(move)
        valeur_au_bout, _ = meilleur_coup_sans_elagage(board_temp, profondeur -1, "noir" if couleur =="blanc" else"blanc") # Pas nécéssairement le meilleur
 
        if couleur == "blanc":
            if valeur_au_bout > meilleur_valeur: # On s'actualise sur la meilleure valeure
                meilleur_valeur = valeur_au_bout
                meilleur_choix = move # Mais ce sera le move en fin d'arbre non ? pas celui actuel ? 
        
        else:
            if valeur_au_bout < meilleur_valeur:
                meilleur_valeur = valeur_au_bout
                meilleur_choix = move

    return meilleur_valeur, meilleur_choix

def meilleur_coup_alpha_beta(board, profondeur, couleur, alpha=-float("inf"), beta=float("inf")):
    if profondeur == 0 or board.is_game_over():
        return eval_position(board), None
    
    meilleur_choix = None

    if couleur == "blanc":
        meilleur_valeur = -float("inf")
        for move in board.legal_moves:
            board_temp = board.copy()
            board_temp.push(move)
            valeur_au_bout, _ = meilleur_coup_alpha_beta(board_temp, profondeur -1, "noir", alpha, beta)
            if valeur_au_bout > meilleur_valeur: 
                meilleur_valeur = valeur_au_bout
                meilleur_choix = move 
            alpha = max(alpha, meilleur_valeur) # On sauvegarde le meilleur coup pour les blancs dans alpha 
            if beta <= alpha: # Cette ligne de code est clé, si le move est inutile d'avance car pas ouf, on break et on élimine la branche
                break


    else:
        meilleur_valeur = float("inf")
        for move in board.legal_moves:
            board_temp = board.copy()
            board_temp.push(move)
            valeur_au_bout, _ = meilleur_coup_alpha_beta(board_temp, profondeur -1, "blanc", alpha, beta)
            if valeur_au_bout < meilleur_valeur:
                meilleur_valeur = valeur_au_bout
                meilleur_choix = move
            beta = min(beta, meilleur_valeur) # On sauvegarde le pire coup pour les blancs dans beta
            if beta <= alpha : 
                break

    return meilleur_valeur, meilleur_choix
    