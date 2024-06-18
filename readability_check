import json
import re
from matplotlib import pyplot as plt
import numpy as np
from readability import Readability
from general_functions import write_boxplot_to_file

DATAPATH = "data"

def get_fleshkincaid(genres):
    for s in genres:
        with open(f'{DATAPATH}/generatedJson/V6_with_interpunction/{s}LyricsInterpunction.jl', 'r') as f:
            song_info = f.readlines()
            song_info = map(json.loads, song_info)

        fleschkincaidScores = []
        for song in song_info:
            # print(song["song"])
            lyrics = song["lyrics"]
            stripped = ''.join([i for i in lyrics if i.isalpha() or i == ' '])
            if len(stripped.strip().split()) >= 100:
                r = Readability(lyrics)
                fleschkc = r.flesch_kincaid()
                fleschkincaidScores.append(fleschkc.score)

        with open (f'{DATAPATH}/fleschkincaid_scores/{s}_readability_interpunction', 'w') as f:
            for score in fleschkincaidScores:
                f.write(str(score) + "\n")
        print(s + " written to file")

def get_spache_and_dalechall(genres):
    for s in genres:
        with open(f'{DATAPATH}/generatedJson/V6_with_interpunction/{s}LyricsInterpunction.jl', 'r') as f:
            song_info = f.readlines()
            song_info = map(json.loads, song_info)

        spacheScores = []
        daleScores = []
        for song in song_info:
            # print(song["song"])
            lyrics = song["lyrics"]
            stripped = ''.join([i for i in lyrics if i.isalpha() or i == ' '])
            if len(stripped.strip().split()) >= 100:
                r = Readability(lyrics)
                spache = r.spache()
                spacheScores.append(spache.score)

                dale = r.dale_chall()
                daleScores.append(dale.score)

        with open (f'{DATAPATH}/spache_scores/{s}_readability_interpunction', 'w') as f:
            for score in spacheScores:
                f.write(str(score) + "\n")

        with open (f'{DATAPATH}/dalechall_scores/{s}_readability_interpunction', 'w') as f:
            for score in daleScores:
                f.write(str(score) + "\n")
        print(s + " written to file")

def get_scores_from_file(genres, folder):
    genreData = []
    for s in genres:
        with open (f'{DATAPATH}/{folder}/{s}_readability_interpunction', 'r') as f:
            probabilitiesStrings = f.readlines()
            probabilities = []
            for prob in probabilitiesStrings:
                if float(prob) <= 20:
                    probabilities.append(float(re.sub('\n', '', prob)))
                else:
                    print("removed outlier at " + prob + " in genre " + s)
            genreData.append(probabilities)
    return genreData

def write_boxplot_info_to_file(genreData, genres, folder):
    genreMap = dict(zip(genres, genreData))
    with open (f'{DATAPATH}/{folder}/BoxplotInfo_interpunction.json', 'w') as f:
        write_boxplot_to_file(genreData, genres, genreMap, f)

def devideListBy(devide, list):
    for i in range(len(list)):
        list[i] = list[i]/devide
    return list

def create_boxplot(genreData):
    fig = plt.figure(figsize =(12, 7))
    ax = fig.add_subplot(111)

    # positions = []
    # pos = 3.5
    # for i in range(5):
    #     positions.append(pos * i - 0.4)
    #     positions.append(pos * i)
    #     positions.append(pos * i + 0.4)
    # positions = [1, 1.5, 2, 3.2, 3.8, 5.2, 5.8, 7.2, 7.8, 9.2, 9.8]
    positions = [0.8, 1.5, 2.2, 3.8, 4.5, 5.2, 6.8, 7.5, 8.2, 9.8, 10.5, 11.2, 12.8, 13.5, 14.2]
    positions = devideListBy(1.25, positions)

    bp = ax.boxplot(genreData, patch_artist = True, notch ='True', vert = 1, positions=positions, widths=0.6)

    # colors = ['#41B8D5', '#2F5F98', '#31356E', '#6CE5E8', '#2D8BBA'] *2
    colors = ['#31356E', '#6CE5E8', '#2D8BBA'] * 5
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    custom_lines = [plt.Line2D([0], [0], color='#31356E', lw=4),
                    plt.Line2D([0], [0], color='#6CE5E8', lw=4),
                    plt.Line2D([0], [0], color='#2D8BBA', lw=4)]
    ax.legend(custom_lines, ['Flesch-Kincaid', 'Spache', 'Dale-Chall'], loc='upper right')


    ax.set_xticks(devideListBy(1.25, [1.5, 4.5, 7.5, 10.5, 13.5]))
    ax.set_xticklabels(["Pop", "Rock", "Country", "Rap", "R&B"])
    # ax.set_xticklabels(["Pop-SP", "Pop-DC", "Rock-SP","Rock-DC", "Country-SP", "Country-DC", "Rap-SP", "Rap-DC", "R&B-SP", "R&B-DC"])
    ax.set_xlabel("Genres")
    ax.set_ylabel("Grade Level")
    plt.show()

genres = ["pop", "rock", "country", "rap", "RB"]
# get_fleshkincaid(genres)
# get_spache_and_dalechall(genres)

# folders = ["fleschkincaid_scores", "spache_scores",  "dalechall_scores"]
# for folder in folders:
#     write_boxplot_info_to_file(get_scores_from_file(genres, folder), genres, folder)

combinedGenreData = []
for data1, data2, data3 in zip(get_scores_from_file(genres, "fleschkincaid_scores"), get_scores_from_file(genres, "spache_scores"), get_scores_from_file(genres, "dalechall_scores")):
    combinedGenreData.append(data1)
    combinedGenreData.append(data2)
    combinedGenreData.append(data3)
create_boxplot(combinedGenreData)

#possibilities: Dale Chall - familiar words, list of 3000 words that are easy, all other words are difficult 
# fleshkincaid doesn't work since it use sentence length and song lyrics often don't contain well stuctured sentences (no .)
