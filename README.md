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
A améliorer : Table de "transposition". Biblio ouverture.¨
A améliorer : Eval position ( sécurité du roi, controle du centre, structure des piions, pièces développées)

bug : dernière rangée et sélection de pièce

elagae et intelligence ! bon ( même si encore des modifs )
maintenant il faut implémenter le rock et permettre de déselectionner une pièce. on va travailler sur le fichier main