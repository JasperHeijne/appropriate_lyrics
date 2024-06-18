import matplotlib.pyplot as plt
import json
import re
import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch.nn.functional as F
import matplotlib.cbook as book
from general_functions import write_boxplot_to_file
from kruskal_willis_dunns import kruskal_dunns
from statannotations.Annotator import Annotator
import seaborn as sns

DATAPATH = "data"

def get_probabilities(genres):
    token = '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'
    model = AutoModelForSequenceClassification.from_pretrained("KoalaAI/HateSpeechDetector", token=token)
    tokenizer = AutoTokenizer.from_pretrained("KoalaAI/HateSpeechDetector", token=token)
    print("~~ Done loading model ~~")

    for s in genres:
        with open(f'{DATAPATH}/generatedJson/V4_no_enters/{s}LyricsFiltered_no_enters_copy.jl', 'r') as f:
            song_info = f.readlines()
            song_info = map(json.loads, song_info)

        for song in song_info:
            lyrics = song["lyrics"]
            inputs = tokenizer(lyrics, return_tensors="pt")
            outputs = model(**inputs)

            logits = outputs.logits
            probabilities = F.softmax(logits, dim=1)

            with open (f'{DATAPATH}/results_hate_speech_scan/{s}HateProbailities', 'a') as f:
                f.write(str(probabilities.tolist()[0][1]) + "\n")

        print(f"~~ {s} is written to file! ~~")

    with open(f'{DATAPATH}/generatedJson/V4_no_enters/rapLyricsFiltered_no_enters_sorted.jl', 'r') as f:
        song_info = f.readlines()
        song_info = map(json.loads, song_info)

    for song in song_info:
        lyrics = song["lyrics"]
        inputs = tokenizer(lyrics, return_tensors="pt")
        outputs = model(**inputs)

        logits = outputs.logits
        probabilities = F.softmax(logits, dim=1)

        with open (f'{DATAPATH}/results_hate_speech_scan/rapHateProbailities', 'a') as f:
            f.write(str(probabilities.tolist()[0][1]) + "\n")
        
    print("~~ Even the rap songs fit!! ~~")

def get_probabilities_from_file(genres):
    genreData = []
    for s in genres:
        with open (f'{DATAPATH}/results_hate_speech_scan/{s}HateProbailitiesGood', 'r') as f:
            probabilitiesStrings = f.readlines()
            probabilities = []
            for prob in probabilitiesStrings:
                probabilities.append(float(re.sub('\n', '', prob)))
            genreData.append(probabilities)
    return genreData

def get_probabilities_from_file_dataframe(genres):
    genreData = []
    labels = []
    for s in genres:
        with open(f'{DATAPATH}/results_hate_speech_scan/{s}HateProbailitiesGood', 'r') as f:
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
    ax.set_ylabel("Probability")
    plt.show()

def create_boxplot_significance(dunn, genreData):
    significance_df = dunn
    df = genreData
    
    # Plotting the boxplot
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.boxplot(x='Genre', y='Values', data=df, ax=ax, palette=['#41B8D5', '#2F5F98', '#31356E', '#6CE5E8', '#2D8BBA'], notch=True)
    
    # Preparing pairs for the annotations
    pairs = [("pop", "rock"), ("pop", "country"), ("pop", "rap"), ("pop", "RB"),
             ("rock", "country"), ("rock", "rap"), ("rock", "RB"),
             ("country", "rap"), ("country", "RB"),
             ("rap", "RB")]
    
    # Creating a list of significance values for the pairs
    p_values = [significance_df.loc[pair[0], pair[1]] for pair in pairs]
    
    # Annotating the plot
    annotator = Annotator(ax, pairs, data=df, x='Genre', y='Values')
    annotator.set_pvalues_and_annotate(p_values)
    
    plt.title("Hate speech per genre")
    plt.show()

def write_boxplot_info_to_file(genreData, genres):
    genreMap = dict(zip(genres, genreData))
    with open (f'{DATAPATH}/results_hate_speech_scan/BoxplotInfo.json', 'w') as f:
        # f.write(json.dumps(book.boxplot_stats(genreData, labels=genres)))
        write_boxplot_to_file(genreData, genres, genreMap, f)

def inverse(genres):
    for s in genres:
        probabilities = []
        with open (f'{DATAPATH}/results_hate_speech_scan/{s}HateProbailities', 'r') as f:
            probabilitiesStrings = f.readlines()
            for prob in probabilitiesStrings:
                probabilities.append(float(re.sub('\n', '', prob)))

        probabilities = map(lambda x: 1 - x, probabilities)

        with open (f'{DATAPATH}/results_hate_speech_scan/{s}HateProbailitiesGood', 'w') as f:
            for prob in list(probabilities):
                f.write(str(prob) + "\n")

genres = ["pop", "rock", "country", "rap", "RB"]

# get_probabilities(genres)
# inverse(genres)
genreData = get_probabilities_from_file(genres)
# genreDataFrame = get_probabilities_from_file_dataframe(genres)

# dunn = kruskal_dunns(genreData=genreData, genreDataFrame=genreDataFrame)
# create_boxplot_significance(dunn=dunn, genreData=genreDataFrame)
# write_boxplot_info_to_file(genreData, genres)
create_boxplot(genreData)
