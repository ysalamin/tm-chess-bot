# TM
Travail de Maturité / Intelligence artificielle aux échecs

Pygame documentation
Youtube
https://python-chess.readthedocs.io/en/latest/core.html
https://python-chess.readthedocs.io/en/latest/



bug : meilleur coup = None. car meilleure valeur = 0 et peut etre aucun coup bat cela donc ca reste none
sol : meilleur coup = float("-inf")

bug : piece = piece_at(case)
sol : faut traduire, là c'est un int et nous on veut


A améliorer : UI ( pièce sélectionnée enlevable, visible, et rock +  victoire)
A améliorer : Alpha-Beta, Eval position avec plus de facteurs. Table de "transposition". Biblio ouverture.

Ou j'en suis : Pour corriger mon erreur, je dois mettre 2 return TJR et comme ça je pourrais tjr accèder à l'eval position ( int) quand j'aurais besoin, et ne pas avoir de problème de type car j'accède au bon.
 return meilleur_valeur, meilleur_choix en bas
 return eval_position(board, couleur), None en haut prof 0
valeur_au_bout, _ = meilleur_coup(board_temp, profondeur -1, couleur_coup_adverse)
