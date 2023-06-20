# TM
Travail de Maturité / Intelligence artificielle aux échecs

Pygame documentation
Youtube
https://python-chess.readthedocs.io/en/latest/core.html

Je me suis arrêté en corrigeant le but des valeurs None. Maintenant il y a d'autres bugs à réglé :D
Point positif : j'ai compris relu et annoté tout le code
bug : meilleur coup = None. car meilleure valeur = 0 et peut etre aucun coup bat cela donc ca reste none
sol : meilleur coup = float("-inf")

bug : piece = piece_at(case)
sol : faut traduire, là c'est un int et nous on veut
problème que je remet à plus tard : au lieu de max et minimiser, j'ai changé le signe jsp si c bien
