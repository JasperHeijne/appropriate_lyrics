import re
import pandas as pd
import scikit_posthocs as posth
from scipy import stats

DATAPATH = "data"

def kruskal_dunns(genreData, genreDataFrame):
    kruskal = stats.kruskal(*genreData)
    print("\nKruskal result: \n" + str(kruskal))

    if (kruskal.pvalue < 0.05):
        dunn = posth.posthoc_dunn(a=genreDataFrame, val_col='Values', group_col='Genre', p_adjust='bonferroni')
        print("\nPost hoc Dunn's: \n" + str(dunn))
        stars_df = dunn.applymap(p_value_to_stars)
        print("\nSignificance: \n" + str(stars_df))
        return dunn
    else:
        print("no significant differences between distributions")

def p_value_to_stars(p):
    if p > 5.00e-02:
        return 'ns'
    elif p > 1.00e-02:
        return '*'
    elif p > 1.00e-03:
        return '**'
    elif p > 1.00e-04:
        return '***'
    else:
        return '****'