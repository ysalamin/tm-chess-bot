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

bug : tour s'efface pas car dimensions du carré foirées, deux fois multipliées

Amélioration :  Jouer noir,  Table de transpo, biblio d'ouverture ( et le vert pk pas)
on va tout remettre en couleur bien propre avec un schéma bien clean

