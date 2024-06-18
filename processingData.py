import json
import re
import pandas as pd

DATAPATH = "data"

def filtering_lyrics():
    genres = ["pop", "rock", "country", "rap", "RB"]
    for s in genres:
        with open(f'{DATAPATH}/generatedJson/{s}LyricsFiltered.jl', 'r') as f:
            song_info = f.readlines()
            song_info = map(json.loads, song_info)
        
        with open (f'{DATAPATH}/generatedJson/V6_with_interpunction/{s}LyricsInterpunction', 'w') as f:
            for song in song_info:
                lyrics = song["lyrics"].strip()
                lyrics = re.sub('\n', '. ', lyrics)
                newSong = {
                    "song": song["song"],
                    "lyrics": lyrics
                }
                f.write(json.dumps(newSong) + "\n")

def changing_the_format_of_the_created_per_genre_files():
    #pop:
    with open(f"{DATAPATH}/generatedJson/V1_1_line_with_list/popLyrics.json", 'r') as input_file:
        # Parse the JSON content into a list of dictionaries
        json_content = json.loads(input_file.readline())

    # Write each JSON object to the output file, one per line
    with open(f"{DATAPATH}/generatedJson/popLyrics2.json", 'w') as output_file:
        for json_obj in json_content:
            # Serialize each JSON object back into a string and write it to the output file
            output_file.write(json.dumps(json_obj) + "\n")
    
    #rock:
    with open(f"{DATAPATH}/generatedJson/V1_1_line_with_list/rockLyrics.json", 'r') as input_file:
        json_content = json.loads(input_file.readline())

    with open(f"{DATAPATH}/generatedJson/rockLyrics2.json", 'w') as output_file:
        for json_obj in json_content:
            output_file.write(json.dumps(json_obj) + "\n")
    
    #country:
    with open(f"{DATAPATH}/generatedJson/V1_1_line_with_list/countryLyrics.json", 'r') as input_file:
        json_content = json.loads(input_file.readline())

    with open(f"{DATAPATH}/generatedJson/countryLyrics2.json", 'w') as output_file:
        for json_obj in json_content:
            output_file.write(json.dumps(json_obj) + "\n")

    #rap:
    with open(f"{DATAPATH}/generatedJson/V1_1_line_with_list/rapLyrics.json", 'r') as input_file:
        json_content = json.loads(input_file.readline())

    with open(f"{DATAPATH}/generatedJson/rapLyrics2.json", 'w') as output_file:
        for json_obj in json_content:
            output_file.write(json.dumps(json_obj) + "\n")
    
    #R&B:
    with open(f"{DATAPATH}/generatedJson/V1_1_line_with_list/RBLyrics.json", 'r') as input_file:
        json_content = json.loads(input_file.readline())

    with open(f"{DATAPATH}/generatedJson/RBLyrics2.json", 'w') as output_file:
        for json_obj in json_content:
            output_file.write(json.dumps(json_obj) + "\n")

def getting_the_lyrics_and_name_and_putting_them_in_the_file_of_the_corresponding_genre():
    with open(f'{DATAPATH}/song_info.jl', 'r') as f:
        song_info = f.readlines()
        song_info = map(json.loads, song_info)
    print("~~~~ read lines from song_info.jl ~~~~")

    with open(f'{DATAPATH}/lyrics.jl', 'r') as f2:
        lyrics = f2.readlines()
        lyrics = map(json.loads, lyrics)
    print("~~~~ read lines from lyrics.jl ~~~~")

    lyricsList = []
    for lyric in lyrics:
        lyricsList.append(lyric)

    popSongs = []
    countrySongs = []
    RBSongs = []
    rapSongs = []
    rockSongs = []

    for song in song_info:
        songName = song["url_name"]
        # print(songName)
        print("next song")
        for lyric in lyricsList:
            # print("b")
            if lyric["song"] == songName:
                print(songName)
                newJsonObject = {
                    "song": songName,
                    "lyrics": lyric["lyrics"]
                    }
                for tag in song["tags"]:
                    if tag == "Pop":
                        popSongs.append(newJsonObject)
                    if tag == "Country":
                        countrySongs.append(newJsonObject)
                    if tag == "R&B":
                        RBSongs.append(newJsonObject)
                    if tag == "Rap":
                        rapSongs.append(newJsonObject)
                    if tag == "Rock":
                        rockSongs.append(newJsonObject)
    
    with open(f"{DATAPATH}/generatedJson/popLyrics.json", "w") as outfile:
        json.dump(popSongs, outfile)
    outfile.close()

    with open(f"{DATAPATH}/generatedJson/countryLyrics.json", "w") as outfile:
        json.dump(countrySongs, outfile)
    outfile.close()

    with open(f"{DATAPATH}/generatedJson/RBLyrics.json", "w") as outfile:
        json.dump(RBSongs, outfile)
    outfile.close()

    with open(f"{DATAPATH}/generatedJson/rapLyrics.json", "w") as outfile:
        json.dump(rapSongs, outfile)
    outfile.close()

    with open(f"{DATAPATH}/generatedJson/rockLyrics.json", "w") as outfile:
        json.dump(rockSongs, outfile)
    outfile.close()

def seperatingLongAndShortSongs():
    with open(f'{DATAPATH}/generatedJson/V4_no_enters/rapLyricsFiltered_no_enters.jl', 'r') as f:
        song_info = f.readlines()
        song_info = map(json.loads, song_info)

    with open (f'{DATAPATH}/generatedJson/V4_no_enters/rapLyricsFiltered_no_enters_long_songs.jl', 'w') as f:
        for song in song_info:
            lyrics = song["lyrics"]
            numWords = len(re.findall(r'\w+', lyrics))
            if numWords > 617:
                newSong = {
                    "song": song["song"],
                    "lyrics": lyrics
                }
                f.write(json.dumps(newSong) + ",\n")

def sorting_on_characters():
    with open(f'{DATAPATH}/generatedJson/V4_no_enters/rapLyricsFiltered_no_enters.jl', 'r') as f:
            song_info = f.readlines()
            song_info = map(json.loads, song_info)

    # Process the songs to count the number of words and prepare for sorting
    songs = []
    for song in song_info:
        lyrics = song["lyrics"]
        numWords = len(lyrics)
        newSong = {
            "song": song["song"],
            "lyrics": lyrics,
            "chars": numWords
        }
        songs.append(newSong)

    # Sort the songs by the number of words in ascending order
    songs.sort(key=lambda x: x["chars"])

    # Write the sorted songs back to the output file without the word count
    with open(f'{DATAPATH}/generatedJson/V4_no_enters/rapLyricsFiltered_no_enters_sorted.jl', 'w') as f:
        for song in songs:
            newSong = {
                "song": song["song"],
                "lyrics": song["lyrics"]
            }
            f.write(json.dumps(newSong) + "\n")

def extract_songs(song_list):
    return {item["song"] for item in song_list}

def overlap():
    genres = ["pop", "rock", "country", "rap", "RB"]
    all_lists = []

    for s in genres:
        with open(f'{DATAPATH}/generatedJson/V4_no_enters/{s}LyricsFiltered_no_enters.jl', 'r') as f:
            song_info = f.readlines()
            song_info = list(map(json.loads, song_info))
        all_lists.append(song_info)
    
    genre_names = ["Pop", "Rock", "Country", "Rap", "R&B"]
    song_sets = [extract_songs(song_list) for song_list in all_lists]

    # Initialize the results table
    results_counts = [[0] * len(all_lists) for _ in range(len(all_lists))]

    results_percentages = [[0.0] * len(all_lists) for _ in range(len(all_lists))]

    # Calculate overlaps
    for i in range(len(all_lists)):
        for j in range(i, len(all_lists)):
            if i == j:
                results_counts[i][j] = len(song_sets[i])
                results_percentages[i][j] = 100.0
            else:
                overlap = song_sets[i].intersection(song_sets[j])
                overlap_count = len(overlap)
                results_counts[i][j] = overlap_count
                results_counts[j][i] = overlap_count
                
                min_len = min(len(song_sets[i]), len(song_sets[j]))
                overlap_percentage = round((overlap_count / min_len) * 100 if min_len > 0 else 0, 2)
                results_percentages[i][j] = overlap_percentage
                results_percentages[j][i] = overlap_percentage

    # Create DataFrames for better visualization
    df_counts = pd.DataFrame(results_counts, index=genre_names, columns=genre_names)
    df_percentages = pd.DataFrame(results_percentages, index=genre_names, columns=genre_names)

    print("Overlap Counts:")
    print(df_counts)
    print("\nOverlap Percentages:")
    print(df_percentages)

filtering_lyrics()
# sorting_on_characters()
# overlap()
