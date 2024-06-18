import matplotlib.pyplot as plt
import json
import re
import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch.nn.functional as F
import matplotlib.cbook as book
from general_functions import write_boxplot_to_file
from kruskal_willis_dunns import kruskal_dunns

DATAPATH = "data"

def get_probabilities(genres):
    token = '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'
    model = AutoModelForSequenceClassification.from_pretrained("KoalaAI/OffensiveSpeechDetector", token=token)
    tokenizer = AutoTokenizer.from_pretrained("KoalaAI/OffensiveSpeechDetector", token=token)
    print("~~ Done loading model ~~")

    for s in genres:
        with open(f'{DATAPATH}/generatedJson/V4_no_enters/{s}LyricsFiltered_no_enters_copy.jl', 'r') as f:
            song_info = f.readlines()
            song_info = map(json.loads, song_info)

        # count = 0
        # allProbabilities = []
        for song in song_info:
            lyrics = song["lyrics"]
            inputs = tokenizer(lyrics, return_tensors="pt")
            outputs = model(**inputs)

            logits = outputs.logits
            probabilities = F.softmax(logits, dim=1)

            with open (f'{DATAPATH}/results_offensive_speech_scan/{s}OffensiveProbailities', 'a') as f:
                f.write(str(probabilities.tolist()[0][1]) + "\n")

            # allProbabilities.append(probabilities.tolist()[0][1])
            # count += 1
            # if count % 50 == 0:
            #     print(f"{s}: {count} songs have been processed")
            # print(str(s) +  ": Non-offensize = " + str(probabilities.tolist()[0][0]) + ", Offensize = " + str(probabilities.tolist()[0][1]) + "\n")

        # with open (f'{DATAPATH}/results_offensive_speech_scan/{s}OffensiveProbailities', 'w') as f:
        #     for prob in allProbabilities:
        #         f.write(str(prob) + "\n")
        print(f"~~ {s} is written to file! ~~")

def get_probabilities_from_file(genres):
    genreData = []
    for s in genres:
        with open (f'{DATAPATH}/results_offensive_speech_scan/{s}OffensiveProbailities', 'r') as f:
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
        with open(f'{DATAPATH}/results_offensive_speech_scan/{s}OffensiveProbailities', 'r') as f:
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

def write_boxplot_info_to_file(genreData, genres):
    genreMap = dict(zip(genres, genreData))
    with open (f'{DATAPATH}/results_offensive_speech_scan/BoxplotInfo.json', 'w') as f:
        # f.write(json.dumps(book.boxplot_stats(genreData, labels=genres)))
        write_boxplot_to_file(genreData, genres, genreMap, f)


# genres = ["rap"]
# genres = ["rap"]
# genres = ["country"]
# get_probabilities(genres)

genres = ["pop", "rock", "country", "rap", "RB"]
genreData = get_probabilities_from_file(genres)
# genreDataFrame = get_probabilities_from_file_dataframe(genres)

# kruskal_dunns(genreData=genreData, genreDataFrame=genreDataFrame)
# write_boxplot_info_to_file(genreData, genres)
create_boxplot(genreData)
