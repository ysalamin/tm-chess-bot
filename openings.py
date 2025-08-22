"""
Small database of the most popular openings
"""
White_Openings = []
Black_Openings = []

# Popular white openings
London = {1: "d2d4", 2: None, 3:"c1f4", 4: None, 5:"e2e3", 6: None, 7:"g1f3"}
Spanish = {1: "e2e4", 2: None, 3:"g1f3", 4: None, 5:"f1b5"}
Italian = {1: "e2e4", 2: None, 3: "g1f3", 4: None, 5:"f1c4"}

# Popular black openings
Sicilian = {1: None, 2: "c7c5", 3: None, 4: "d7d6"}
French = {1: None, 2: "e7e6", 3: None, 4: "d7d5"}
CaroKann = {1: None, 2: "c7c6", 3: None, 4: "d7d5"}

White_Openings.extend([London, Spanish, Italian])

Black_Openings.extend([Sicilian, French, CaroKann])
