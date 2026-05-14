# =============================================== AHP method ===============================
from pymcdm.weights.subjective import AHP
import numpy as np


answers = {(0, 1): 0.14285714285714285, (0, 2): 4, (0, 3): 4, (0, 4): 7, (0, 5): 3, (0, 6): 5, (0, 7): 5, (0, 8): 0.25, (1, 2): 4, (1, 3): 4, (1, 4): 1, (1, 5): 0.16666666666666666, (1, 6): 0.14285714285714285, (1, 7): 0.14285714285714285}
values = np.array(list(answers.values()))
matrix_criteria = [
    "Rodzaj bólu",
    "Intensywność bólu",
    "Ogólna elastyczność ciała",
    "Sprawność fizyczna",
    "Menstruacja",
    "Ciąża",
    "Nadciśnienie",
    "Doświadczenie w jodze",
    "Samopoczucie psychiczne"
]

ahp = AHP(scoring=values)
weights = ahp()
cr = ahp.get_cr()
print(weights)
print(cr)


