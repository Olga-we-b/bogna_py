import numpy as np
from pymcdm.weights.subjective import AHP, RANCOM
import pandas as pd

answers = {(0, 1): 0.14285714285714285, (0, 2): 4, (0, 3): 4, (0, 4): 7, (0, 5): 3, (0, 6): 5, (0, 7): 5, (0, 8): 0.25, (1, 2): 4, (1, 3): 4, (1, 4): 1, (1, 5): 0.16666666666666666, (1, 6): 0.14285714285714285, (1, 7): 0.14285714285714285}


def ahp_method(user_answers):
    values = np.array(list(user_answers.values()))

    ahp = AHP(scoring=values)

    weights = ahp()

    cr = ahp.get_cr()

    print(f"weights = {weights}, cr = {cr}")
    return weights, cr

def save_answers_to_csv(user_answers, criteria, weights, cr):
    n = len(criteria)

    matrix = np.ones((n, n))

    for (i, j), value in user_answers.items():
        matrix[i][j] = value
        matrix[j][i] = 1 / value

    df_matrix = pd.DataFrame(
        matrix,
        columns=criteria,
        index=criteria
    )
    df_weights = pd.DataFrame({
        'criterion': criteria,
        'weight': weights
    })

    df_cr = pd.DataFrame({
        'criterion': ['CR'],
        'weight': [cr]
    })

    with open('results.csv', 'w', encoding='utf-8-sig') as f:
        f.write('AHP comparison matrix \n')
        df_matrix.to_csv(f)

        f.write('\n\n')

        f.write('Weights')
        df_weights.to_csv(f, index=False)

        f.write('\n')

        df_cr.to_csv(f, index=False, sep=';')
        f.write('\n')

    return df_matrix, df_weights

