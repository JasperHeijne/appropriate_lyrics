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
from general_functions import write_boxplot_to_file
import statistics

DATAPATH = "data"

def get_probabilities_from_file(genres):
    genreData = []
    for s in genres:
        with open (f'{DATAPATH}/results_curse_words_proportions/{s}Proportions', 'r') as f:
            probabilitiesStrings = f.readlines()
            probabilities = []
            for prob in probabilitiesStrings:
                probabilities.append(float(re.sub('\n', '', prob)) * 100)
            genreData.append(probabilities)
    return genreData

def get_probabilities_from_file_dataframe(genres):
    genreData = []
    labels = []
    for s in genres:
        with open(f'{DATAPATH}/results_curse_words_proportions/{s}Proportions', 'r') as f:
            probabilitiesStrings = f.readlines()
            probabilities = [float(re.sub('\n', '', prob)) * 100 for prob in probabilitiesStrings]
            genreData.extend(probabilities)
            labels.extend([s] * len(probabilities))
    
    df = pd.DataFrame({'Genre': labels, 'Values': genreData})
    return df

def create_boxplot(genreData):
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(genreData, patch_artist = True,
                    notch ='True', vert = 1)

    colors = ['#41B8D5', '#2F5F98', '#31356E', '#6CE5E8', '#2D8BBA']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    ax.set_xticklabels(["Pop", "Rock", "Country", "Rap", "R&B"])
    ax.set_xlabel("Genres")
    ax.set_ylabel("Percentage")
    plt.show()

def write_boxplot_info_to_file(genreData, genres): #["pop", "rock", "country", "rap", "RB"]
    genreMap = dict(zip(genres, genreData))
    with open (f'{DATAPATH}/results_curse_words_proportions/BoxplotInfo.json', 'w') as f:
        # f.write(json.dumps(book.boxplot_stats(genreData, labels=genres)))
        write_boxplot_to_file(genreData, genres, genreMap, f)

def create_csv(genreData):
    # Create a DataFrame from the list of lists with column names
    # Assuming we name the columns 'Column1', 'Column2', etc.
    probabilities = genreData
    genres = [1, 2, 3, 4, 5] #[1 = "Pop", 2 = "Rock", 3 = "Country", 4 = "Rap", 5 = "RB"]

    # Flatten the data and create rows for the DataFrame
    data = []
    for i, genre in enumerate(genres):
        for song_index, probability in enumerate(probabilities[i]):
            data.append({"song": song_index + 1, "genre": genre, "percentage": probability})

    # Create the DataFrame
    df = pd.DataFrame(data)

    # Write the DataFrame to a CSV file
    df.to_csv(f'{DATAPATH}/results_curse_words_proportions/allCurseWords.csv', index=False)

    print("CSV file created successfully.")

def create_boxplot_significance(genres, genreData):
    data = []
    labels = []
    for genre, values in zip(genres, genreData):
        data.extend(values)
        labels.extend([genre] * len(values))

    df = pd.DataFrame({'Genre': labels, 'Values': data})

    fig, ax = plt.subplots(figsize=(10, 10))
    pal = ['#41B8D5', '#2F5F98', '#31356E', '#6CE5E8', '#2D8BBA']
    sns.boxplot(x='Genre', y='Values', data=df, ax=ax, palette=pal, linewidth=1)

    pairs = [
        ("Pop", "Rock"),
        ("Pop", "Country"),
        ("Pop", "Rap"),
        ("Pop", "R&B"),
        ("Rock", "Country"),
        ("Rock", "Rap"),
        ("Rock", "R&B"),
        ("Country", "Rap"),
        ("Country", "R&B"),
        ("Rap", "R&B")
    ]

    annotator = Annotator(ax, pairs, data=df, x='Genre', y='Values')
    annotator.configure(test='Kruskal', text_format='star', loc='inside', comparisons_correction="bonferroni")
    annotator.apply_and_annotate()

    plt.title("Curse words per genre")
    plt.show()

genresNames = ["Pop", "Rock", "Country", "Rap", "R&B"]
genresFileName = ["pop", "rock", "country", "rap", "RB"]

genreData = get_probabilities_from_file(genresFileName)
# genreDataFrame = get_probabilities_from_file_dataframe(genresFileName)

# kruskal_dunns(genreData=genreData, genreDataFrame=genreDataFrame)
# create_boxplot_significance(genresNames, genreData)
# write_boxplot_info_to_file(genreData, genresFileName)
create_boxplot(genreData)

# create_csv(genreData)