import pandas as pd
import profanity_check as check
import json
import re
import matplotlib.pyplot as plt
import matplotlib.cbook as book
from general_functions import write_boxplot_to_file
from kruskal_willis_dunns import kruskal_dunns

DATAPATH = "data"

# Getting the probabilities values for the entire lyrics:
def get_probabilities(genres):
    for s in genres:
        with open(f'{DATAPATH}/generatedJson/V4_no_enters/{s}LyricsFiltered_no_enters.jl', 'r') as f:
            song_info = f.readlines()
            song_info = map(json.loads, song_info)

        allProfanities = []
        for song in song_info:
            lyrics = song["lyrics"]
            profanityProb = check.predict_prob([lyrics])
            allProfanities.append(profanityProb[0])
        
        # total = 0
        # for prob in allProfanities:
        #     total += prob
        # print ("average profanity: " + str(total/len(allProfanities)))

        with open (f'{DATAPATH}/results_profanity_check_scan/{s}ProfanityProbailities', 'w') as f:
            for prob in  allProfanities:
                f.write(str(prob) + "\n")

def get_probabilities_from_file(genres):
    genreData = []
    for s in genres:
        with open (f'{DATAPATH}/results_profanity_check_scan/{s}ProfanityProbailities', 'r') as f:
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
        with open(f'{DATAPATH}/results_profanity_check_scan/{s}ProfanityProbailities', 'r') as f:
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
    with open (f'{DATAPATH}/results_profanity_check_scan/BoxplotInfo.json', 'w') as f:
        # f.write(json.dumps(book.boxplot_stats(genreData, labels=genres)))
        write_boxplot_to_file(genreData, genres, genreMap, f)

genres = ["pop", "rock", "country", "rap", "RB"]
# genreData = get_probabilities_from_file(genres)
# create_boxplot(genreData)
# genreDataFrame = get_probabilities_from_file_dataframe(genres)
# kruskal_dunns(genreData=genreData, genreDataFrame=genreDataFrame)
# write_boxplot_info_to_file(genreData, genres)
testSong = "\n\n\n\ub0b4\uac00 \ub0a0 \ub208\uce58\ucc58\ub358 \uc21c\uac04\n\ub5a0\ub098\uc57c\ub9cc \ud588\uc5b4\n\ub09c \ucc3e\uc544\ub0b4\uc57c \ud588\uc5b4\nAll day all night\n\n\n\uc0ac\ub9c9\uacfc \ubc14\ub2e4\ub4e4\uc744 \uac74\ub108\n\ub113\uace0 \ub113\uc740 \uc138\uacc4\ub97c\n\ud5e4\ub9e4\uc5b4 \ub2e4\ub154\uc5b4\nBaby I\n\n\nI could make it better\nI could hold you tighter\n\uadf8 \uba3c \uae38 \uc704\uc5d0\uc11c\nOh you're the light\n\n\n\ucd08\ub300\ubc1b\uc9c0 \ubabb\ud55c\n\ud658\uc601\ubc1b\uc9c0 \ubabb\ud55c\n\ub098\ub97c \uc54c\uc544\uc92c\ub358 \ub2e8 \ud55c \uc0ac\ub78c\n\n\n\ub05d\ub3c4 \ubcf4\uc774\uc9c0 \uc54a\ub358 \uc601\uc6d0\uc758 \ubc24\n\ub0b4\uac8c \uc544\uce68\uc744 \uc120\ubb3c\ud55c \uac74 \ub108\uc57c\n\uc774\uc81c \uadf8 \uc190 \ub0b4\uac00 \uc7a1\uc544\ub3c4 \ub420\uae4c\nOh oh\nI can make it right\n\n\nAll right\nAll right\nOh I can make it right\n\n\nAll right\nAll right\nOh I can make it right\n\n\n\uc774 \uc138\uc0c1 \uc18d\uc5d0 \uc601\uc6c5\uc774 \ub41c \ub098\n\ub098\ub97c \ucc3e\ub294 \ud070 \ud658\ud638\uc640\n\ub0b4 \uc190, \ud2b8\ub85c\ud53c\uc640 \uae08\ube5b \ub9c8\uc774\ud06c\nAll day, everywhere\nBut \ubaa8\ub4e0 \uac8c \ub108\uc5d0\uac8c \ub2ff\uae30 \uc704\ud568\uc778 \uac78\n\ub0b4 \uc5ec\uc815\uc758 \ub2f5\uc778 \uac78\n\ub110 \ucc3e\uae30 \uc704\ud574 \ub178\ub798\ud574\nBaby to you\n\n\n\uc804\ubcf4\ub2e4 \uc870\uae08 \ub354 \ucee4\uc9c4 \ud0a4\uc5d0\n\uc880 \ub354 \ub2e8\ub2e8\ud574\uc9c4 \ubaa9\uc18c\ub9ac\uc5d0\n\ubaa8\ub4e0 \uac74 \ub124\uac8c \ub3cc\uc544\uac00\uae30 \uc704\ud574\n\uc774\uc81c \ub108\ub77c\ub294 \uc9c0\ub3c4\ub97c \ud65c\uc9dd \ud3bc\uce60\uac8c\nMy rehab\n\ub0a0 \ubd10 \uc65c \ubabb \uc54c\uc544\ubd10\n\ub0a8\ub4e4\uc758 \uc544\uc6b0\uc131 \ub530\uc704 \ub098 \ub4e3\uace0 \uc2f6\uc9c0 \uc54a\uc544\n\ub108\uc758 \ud5a5\uae30\ub294 \uc5ec\uc804\ud788 \ub098\ub97c \uaff0\ub6ab\uc5b4 \ubb34\ub108\ub728\ub824\n\ub418\ub3cc\uc544\uac00\uc790 \uadf8\ub54c\ub85c\n\n\nBaby I know\nI can make it better\nI can hold you tighter\n\uadf8 \ubaa8\ub4e0 \uae38\uc740 \ub110\n\ud5a5\ud55c \uac70\uc57c\n\n\n\ub2e4 \uc18c\uc6a9\uc5c6\uc5c8\uc5b4\n\ub108 \uc544\ub2cc \ub2e4\ub978 \uac74\n\uadf8\ub54c\ucc98\ub7fc \ub0a0 \uc5b4\ub8e8\ub9cc\uc838\uc918\n\n\n\ub05d\ub3c4 \ubcf4\uc774\uc9c0 \uc54a\ub358 \uc601\uc6d0\uc758 \ubc24\n\ub0b4\uac8c \uc544\uce68\uc744 \uc120\ubb3c\ud55c \uac74 \ub108\uc57c\n\uc774\uc81c \uadf8 \uc190 \ub0b4\uac00 \uc7a1\uc544\ub3c4 \ub420\uae4c\nOh oh\nI can make it right\n\n\nAll right\nAll right\nOh I can make it right\n\n\nAll right\nAll right\nOh I can make it right\n\n\n\uc5ec\uc804\ud788 \uc544\ub984\ub2e4\uc6b4 \ub108\n\uadf8\ub0a0\uc758 \uadf8\ub54c\ucc98\ub7fc \ub9d0\uc5c6\uc774 \uadf8\ub0e5 \ub0a0 \uc548\uc544\uc918\n\uc9c0\uc625\uc5d0\uc11c \ub0b4\uac00 \uc0b4\uc544 \ub0a8\uc740 \uac74\n\ub0a0 \uc704\ud588\ub358 \uac8c \uc544\ub2cc \ub418\ub824 \ub108\ub97c \uc704\ud55c \uac70\ub780 \uac78\n\uc548\ub2e4\uba74 \uc8fc\uc800 \ub9d0\uace0 please save my life\n\ub108 \uc5c6\uc774 \ud5e4\uccd0\uc654\ub358 \uc0ac\ub9c9 \uc704\ub294 \ubaa9\ub9d0\ub77c\n\uadf8\ub7ec\ub2c8 \uc5b4\uc11c \ube68\ub9ac \ub0a0 \uc7a1\uc544\uc918\n\ub108 \uc5c6\ub294 \ubc14\ub2e4\ub294 \uacb0\uad6d \uc0ac\ub9c9\uacfc \uac19\uc744 \uac70\ub780 \uac78 \uc54c\uc544\n\n\nAll right\nI can make it better\nI can hold you tighter\nOh I can make it right\n\n\n\ub2e4 \uc18c\uc6a9\uc5c6\uc5c8\uc5b4\n\ub108 \uc544\ub2cc \ub2e4\ub978 \uac74\nOh I can make it right\n\n[Jungkook, Jimin, V]\nAll right\nAll right\nOh I can make it right\n\n"
print(check.predict_prob([testSong]))