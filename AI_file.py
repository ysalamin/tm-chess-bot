"""
    Partie du code qui s'occupe de la partie IA
"""
import chess

# Attribuer une valeur à chaque pièce
valeurs = {"P": 1, "N": 3.05, "B" : 3.33, "R": 5.63, "Q": 9.5, "K": 1000}

# Faire une fonction d'évaluation de position
def eval_position(pos):
    """
    Evalue un échiquier en lui attribuant une valeur

    Args:
        pos (board): position

    Returns:
        float: valeur associée à la position
    """

    valeur_totale = 0
    valeur_materielle = 0
    valeur_tactique = 0
    #####
    if pos.is_checkmate():
        print("test 1")
        if pos.turn:
            print("test 2")
            valeur_totale = -10000
            return valeur_totale
        else:
            valeur_totale = 10000
            return valeur_totale
    ######
    # Valeur matérielle
    for case in range(64):
        piece = pos.piece_at(case)

        if piece is not None:
            piece_value = valeurs[str(piece).upper()]

            valeur_materielle += piece_value if (piece.color == chess.WHITE) else -piece_value

    # Valeur tactique
    moves_possibles = pos.legal_moves
    for move in moves_possibles:
        piece = pos.piece_at(move.from_square)
        if piece is not None:
            valeur_tactique += 1 if (piece.color == chess.WHITE) else -1



    valeur_totale = valeur_materielle + valeur_tactique * 0.1

    return valeur_totale


def meilleur_coup_alpha_beta(board, profondeur, couleur, alpha=-float("inf"), beta=float("inf")):
    """
    Fonction qui utilise l'algorithme minmax ainsi que l'élagage alpha beta
    afin de calculer toutes les positions non élaguées à une profondeur de X.

    Args:
        board (board): position
        profondeur (int): profondeur de calcul / nombre de fois où le principe de récursivité
        va s'éffectuer
        couleur (booléen): couleur qui joue
        alpha (float, optional): nombre, cherchant toujours à s'aggrandir et commençant à - l'infini
        beta (float, optional): nombre, cherchant toujours à se rapticir, et commençant à + l'infini

    Returns:
        float: meilleure valeure
        coup: meilleur coup, qui correspond à la meilleur valeure
    """
    if profondeur == 0 or board.is_game_over():
        return eval_position(board), None

    meilleur_choix = None

    if couleur is True:
        meilleur_valeur = -float("inf")
        for move in board.legal_moves:
            board_temp = board.copy()
            board_temp.push(move)
            valeur_au_bout, _ = meilleur_coup_alpha_beta(board_temp, profondeur -1, False, alpha, beta)
            if valeur_au_bout > meilleur_valeur:
                meilleur_valeur = valeur_au_bout
                meilleur_choix = move
            alpha = max(alpha, meilleur_valeur)
            if beta <= alpha:
                break


    else:
        meilleur_valeur = float("inf")
        for move in board.legal_moves:
            board_temp = board.copy()
            board_temp.push(move)
            valeur_au_bout, _ = meilleur_coup_alpha_beta(board_temp, profondeur -1, True, alpha, beta)
            if valeur_au_bout < meilleur_valeur:
                meilleur_valeur = valeur_au_bout
                meilleur_choix = move
            beta = min(beta, meilleur_valeur) # On sauvegarde le pire coup pour les blancs dans beta
            if beta <= alpha :
                break

    return meilleur_valeur, meilleur_choix
    