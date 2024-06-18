import math
import profanity_check as check
import json
import re
import matplotlib.pyplot as plt
import matplotlib.cbook as book
import pandas as pd
import numpy as np
import seaborn as sns
from statannotations.Annotator import Annotator
from scipy import stats
import scikit_posthocs as posth
from kruskal_willis_dunns import kruskal_dunns
import statistics

DATAPATH = "data"

def write_boxplot_to_file(genreData, genres, genreMap, f):
    for boxJson in book.boxplot_stats(genreData, labels=genres):
            variance = statistics.variance(genreMap[boxJson["label"]])
            result = {
                "genre": boxJson["label"],
                "median": boxJson["med"],
                "mean": boxJson["mean"],
                "q1": boxJson["q1"],
                "q3": boxJson["q3"],
                "num_outliers": len(boxJson["fliers"]),
                "low_whisk": boxJson["whislo"],
                "high_whisk": boxJson["whishi"],
                "variance": variance,
                "CV": math.sqrt(variance) / boxJson["mean"]
            }
            f.write(json.dumps(result) + ",\n")