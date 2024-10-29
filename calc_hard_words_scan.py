import json
import time
import datetime
# from calc_hard_words import get_hard_words_from_list
from calc_hard_words_parallel import get_hard_words_parallel

DATAPATH = "data"

def get_probabilities(genres):
    for s in genres:
        with open(f'{DATAPATH}/generatedJson/V4_no_enters/{s}LyricsFiltered_no_enters.jl', 'r') as f:
            song_info = f.readlines()
            lyrics_list = [json.loads(line)["lyrics"] for line in song_info]

        start = time.time()
        print("Read all lines in " + s + ", at time: " + str(datetime.datetime.fromtimestamp(start)))

        # prop, nums = get_hard_words_from_list(lyrics_list)
        prop, nums = get_hard_words_parallel(lyrics_list)

        end = time.time()
        print("Computed proportion and number of hard words, at time: " + str(datetime.datetime.fromtimestamp(end)))
        print("Total time: " + str(end - start) + " seconds")

        with open ('data/results_hard_words_scan/HardWords.py', 'a') as f:
            f.write(f"\nproportions_{s} = " + str(prop) + f"\nnumber_{s} = " + str(nums))

# genres = ["RB"]
# # genres = ["country", "pop"]
# # get_probabilities(genres)

# if __name__ == "__main__":
#     for s in genres:
#         with open(f'{DATAPATH}/generatedJson/V4_no_enters/{s}LyricsFiltered_no_enters.jl', 'r') as f:
#             song_info = f.readlines()
#             lyrics_list = [json.loads(line)["lyrics"] for line in song_info]

#         start = time.time()
#         print("Read all lines in " + s + ", at time: " + str(datetime.datetime.fromtimestamp(start)))

#         # prop, nums = get_hard_words_from_list(lyrics_list)
#         prop, nums = get_hard_words_parallel(lyrics_list)

#         end = time.time()
#         print("Computed proportion and number of hard words, at time: " + str(datetime.datetime.fromtimestamp(end)))
#         print("Total time: " + str(end - start) + " seconds")

#         print(f"\nproportions_{s} = " + str(prop) + f"\nnumber_{s} = " + str(nums))

#         with open ('data/results_hard_words_scan/HardWords.py', 'a') as f:
#             f.write(f"\nproportions_{s} = " + str(prop) + f"\nnumber_{s} = " + str(nums))

genres = ["rap"]
if __name__ == "__main__":
    for s in genres:
        with open(f'{DATAPATH}/generatedJson/V4_no_enters/{s}LyricsFiltered_no_enters.jl', 'r') as f:
            song_info = f.readlines()
            lyrics_list = [json.loads(line)["lyrics"] for line in song_info]

        start = 30000
        to = 35000
        while (to <= 30000):
            prop, nums = get_hard_words_parallel(lyrics_list[start : to])

            print(f"\nproportions_{s}_{start}-{to} = " + str(prop) + f"\nnumber_{s}_{start}-{to} = " + str(nums))

            start = to
            to += 5000
        
            print(f"\nproportions_{s}_{start}-{to} = " + str(prop) + f"\nnumber_{s}_{start}-{to} = " + str(nums))

            with open ('data/results_hard_words_scan/rapProportions', 'a') as f:
                f.write(str(prop) + "\n")

            with open ('data/results_hard_words_scan/rapNumbers', 'a') as f:
                f.write(str(nums) + "\n")

        prop, nums = get_hard_words_parallel(lyrics_list[start:])
    
        print(f"\nproportions_{s}>{start} = " + str(prop) + f"\nnumber_{s}>{start} = " + str(nums))

        with open ('data/results_hard_words_scan/rapProportions', 'a') as f:
            f.write(str(prop))

        with open ('data/results_hard_words_scan/rapNumbers', 'a') as f:
            f.write(str(nums))