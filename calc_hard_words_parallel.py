import string
from string import punctuation
import re
import nltk

# Script adapted from https://github.com/BSU-CAST/phonemic_feature_functions/tree/main

#When running for the first time, run in a python console:
# import nltk
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')

import pandas as pd
import numpy as np
import sklearn
import json
import pickle
import json
import os
from nltk.tokenize import SyllableTokenizer
from nltk.corpus import stopwords
import sys
import ssl
import pathlib
from pathlib import Path

def get_POS(row):

    retList = []

    for tag in nltk.pos_tag(row):
        retList.append(tag[1])

    return retList

SSP = SyllableTokenizer()
def magic_e(word):
    result = SSP.tokenize(word)
    syll_count = len(result)
    if syll_count == 1:
        return syll_count
    if re.search('e$', result[len(result) - 1]):
        modified = ''.join([result[i] for i in [len(result) - 2, len(result) - 1]])
        result[len(result) - 2] = modified
        del result[len(result) - 1]
        syll_count = len(result)
    return syll_count

SSP = SyllableTokenizer()
def magic_e_result(word):
    result = SSP.tokenize(word)
    if re.search('e$', result[len(result) - 1]):
        modified = ''.join([result[i] for i in [len(result) - 2, len(result) - 1]])
        result[len(result) - 2] = modified
        del result[len(result) - 1]
    return result

lines = []
import csv

#https://github.com/open-dict-data/ipa-dict
# import pandas as pd
# file_path = 'en_US.txt'
# data_list = []
# with open(file_path, 'r', encoding='utf-8') as file:
#     for line in file:
#         line = line.strip()
#         key, value = line.split('\t')
#         data_list.append((key, value))

# df = pd.DataFrame(data_list, columns=['word', 'phon'])
# print(df)

# file_path = 'phoneticDictionary.csv'
# df.to_csv(file_path, index=False)
        
df = pd.read_csv('phoneticDictionary.csv')
df = pd.DataFrame(list(zip(df['word'], df['phon'])), columns=['word', 'ipa'])

def ipa_word(word):
    this_word = ''
    ipa_word = list(df['word'])
    ipa_notation = list(df['ipa'])
    ipa_dict = dict(zip(ipa_word, ipa_notation))
    if word in ipa_dict.keys():
        this_word = ipa_dict[word].replace("ˈ", "")
        this_word = this_word.replace("ˌ", "")
    return this_word


def check_assimilated_row(row):
    assimilated = 0
    retWords = []
    for word in row:
        if len(magic_e_result(word)) > 1:
            if re.search('^ill', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^imm[aeiou]', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^imp', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^irr[aeiou]', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^suff', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^supp', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^succ', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^surr', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^coll', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^corr', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^att', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^aff', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^agg', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^all', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^ann', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^app', word):
                if not re.search('apples', word):
                    assimilated += 1
                    if word not in retWords:
                        retWords.append(word)
            if re.search('^ass', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^arr', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^diff', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^eff', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^opp', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^off', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)
            if re.search('^occ', word):
                assimilated += 1
                if word not in retWords:
                    retWords.append(word)

    return retWords

def check_adv_suffix_word(row, pos):

    adjs_nouns = ['JJR', 'JJS', 'JJ', 'NN', 'NNP', 'NNS']
    verbs = ['VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP']

    adj_n_suffix = ['ɛɹi$', 'ɔɹi$', 'ənsi$', 'əns$', 'ʒən', 'ʒən', 'ʃən', 'əbəɫ$', 'əbɫi$']
    v_suffix = ['aɪz', 'ɪfaɪ', 'əfaɪ']

    ipa = []
    ret_dict = {}
    for word in row:
        ipa.append(ipa_word(word))
        ret_dict[ipa_word(word)] = word
    i = 0
    retWords = []
    for word in ipa:
        if len(word) > 0:
            if magic_e(row[i]) > 1:
                if pos[i] in adjs_nouns:
                    for suf in adj_n_suffix:
                        if re.search(suf, word):
                            if ret_dict[word] not in retWords:
                                retWords.append(ret_dict[word])
                if pos[i] in verbs:
                    for suf in v_suffix:
                        if re.search(suf, word):
                            if ret_dict[word] not in retWords:
                                retWords.append(ret_dict[word])

        i += 1

    return retWords

COMPOUND_WORDS = ['aircraft', 'airline', 'airmail', 'airplane', 'airport', 'airtight', 'anybody', 'anymore', 'anyone',
                 'anyplace', 'anything', 'anywhere', 'anyhow', 'backboard', 'backbone', 'backfire', 'background',
                 'backpack', 'backward', 'backyard', 'bareback', 'feedback', 'flashback', 'hatchback', 'paperback',
                 'piggyback', 'bathrobe', 'bathroom', 'bathtub', 'birdbath', 'bedrock', 'bedroom', 'bedside',
                 'bedspread', 'bedtime', 'flatbed', 'hotbed', 'sickbed', 'waterbed', 'birthday', 'birthmark',
                 'birthplace', 'birthstone', 'childbirth', 'blackberry', 'blackmail', 'blacksmith', 'blacktop',
                 'bookcase', 'bookkeeper', 'bookmark', 'bookworm', 'checkbook', 'cookbook', 'scrapbook', 'textbook',
                 'buttercup', 'butterfly', 'buttermilk', 'butterscotch', 'doorbell', 'doorknob', 'doorman', 'doormat',
                 'doorstop', 'doorway', 'backdoor', 'outdoor', 'downcast', 'downhill', 'download', 'downpour',
                 'downright', 'downsize', 'downstairs', 'downstream', 'downtown', 'breakdown', 'countdown', 'sundown',
                 'touchdown', 'eyeball', 'eyebrow', 'eyeglasses', 'eyelash', 'eyelid', 'eyesight', 'eyewitness',
                 'shuteye', 'firearm', 'firecracker', 'firefighter', 'firefly', 'firehouse', 'fireman', 'fireplace',
                 'fireproof', 'fireside', 'firewood', 'fireworks', 'backfire', 'bonfire', 'campfire', 'football',
                 'foothill', 'foothold', 'footlights', 'footnote', 'footprint', 'footstep', 'footstool', 'barefoot',
                 'tenderfoot', 'grandchildren', 'granddaughter', 'grandfather', 'grandmother', 'grandparent',
                 'grandson', 'haircut', 'hairdo', 'hairdresser', 'hairpin', 'hairstyle', 'handbag', 'handball',
                 'handbook', 'handcuffs', 'handmade', 'handout', 'handshake', 'handspring', 'handstand',
                 'handwriting', 'backhand', 'firsthand', 'secondhand', 'underhand', 'headache', 'headband',
                 'headdress', 'headfirst', 'headlight', 'headline', 'headlong', 'headmaster', 'headphones',
                 'headquarters', 'headstart', 'headstrong', 'headway', 'airhead', 'blockhead', 'figurehead',
                 'homeland', 'homemade', 'homemaker', 'homeroom', 'homesick', 'homespun', 'homestead', 'homework',
                 'horseback', 'horsefly', 'horseman', 'horseplay', 'horsepower', 'horseshoe', 'racehorse', 'sawhorse',
                 'houseboat', 'housefly', 'housewife', 'housework', 'housetop', 'birdhouse', 'clubhouse', 'doghouse',
                 'greenhouse', 'townhouse', 'landfill', 'landlady', 'landlord', 'landmark', 'landscape', 'landslide',
                 'dreamland', 'farmland', 'highland', 'wasteland', 'wonderland', 'lifeboat', 'lifeguard',
                 'lifejacket', 'lifelike', 'lifelong', 'lifestyle', 'lifetime', 'nightlife', 'wildlife', 'lighthouse',
                 'lightweight', 'daylight', 'flashlight', 'headlight', 'moonlight', 'spotlight', 'sunlight',
                 'mailman', 'snowman', 'gentleman', 'handyman', 'policeman', 'salesman', 'nightfall', 'nightgown',
                 'nightmare', 'nightlight', 'nighttime', 'overnight', 'outbreak', 'outcast', 'outcome', 'outcry',
                 'outdated', 'outdo', 'outdoors', 'outfield', 'outfit', 'outgrow', 'outlaw', 'outline', 'outlook',
                 'outnumber', 'outpost', 'outrage', 'outright', 'outside', 'outsmart', 'outwit', 'blowout',
                 'carryout', 'cookout', 'handout', 'hideout', 'workout', 'lookout', 'overall', 'overboard',
                 'overcast', 'overcome', 'overflow', 'overhead', 'overlook', 'overview', 'playground', 'playhouse',
                 'playmate', 'playpen', 'playroom', 'playwright', 'rainbow', 'raincoat', 'raindrop', 'rainfall',
                 'rainstorm', 'roadblock', 'roadway', 'roadwork', 'railroad', 'sandbag', 'sandbar', 'sandbox',
                 'sandpaper', 'sandpiper', 'sandstone', 'seacoast', 'seafood', 'seagull', 'seaman', 'seaport',
                 'seasick', 'seashore', 'seaside', 'seaweed', 'snowball', 'snowflake', 'snowplow', 'snowshoe',
                 'snowstorm', 'somebody', 'someone', 'someday', 'somehow', 'somewhere', 'something', 'sometime',
                 'underline', 'undergo', 'underground', 'undermine', 'underwater', 'watercolor', 'waterfall',
                 'watermelon', 'waterproof', 'saltwater', 'windfall', 'windmill', 'windpipe', 'windshield',
                 'windswept', 'downwind', 'headwind']

def easy_check_compound(row):

    compounds = []
    for word in row:
        if word in COMPOUND_WORDS:
            if word not in compounds:
                compounds.append(word)

    return compounds

def check_adv_inflectional_verb_row(text_POS):

    verb_tags = ['VBD', 'VBG', 'VBN', 'VBZ']
    inflectional = []

    for item in text_POS:
        if item[1] in verb_tags:
            if re.search('ing$', item[0]):
                inflectional.append(item[0])
            if re.search('ed$', item[0]):
                inflectional.append(item[0])

    return inflectional

def check_adv_inflectional_adj_row(text_POS):

    adj_tags = ['JJR', 'JJS', 'RBR', 'RBS', 'JJ', 'RB']
    inflectional = []

    for item in text_POS:
        if len(item[0]) > 4:
            if item[1] in adj_tags:
                if item[1] == 'JJ':
                    if re.search('ful$', item[0]):
                        if item[0] not in inflectional:
                            inflectional.append(item[0])
                    if re.search('ness$', item[0]):
                        if item[0] not in inflectional:
                            inflectional.append(item[0])
                    if re.search('less$', item[0]):
                        if item[0] not in inflectional:
                            inflectional.append(item[0])
                    if re.search('ily$', item[0]):
                        if item[0] not in inflectional:
                            inflectional.append(item[0])
                else:
                    if item[0] not in inflectional:
                        inflectional.append(item[0])

    return inflectional

def calculate(snippet, simplify=True):

    text = re.sub(r'[^\w\s]', '', snippet)
    text = text.lower().split()
    if simplify:
        text = list(set(text))
        # Remove stop words
        text = [word for word in text if word not in stopwords.words('english')]
    num_words = len(text)
    pos = get_POS(text)
    text_POS = list(zip(text, pos))

    assim = check_assimilated_row(text)
    adv_suf = check_adv_suffix_word(text, pos)
    compound_words = easy_check_compound(text)
    inf_verb = check_adv_inflectional_verb_row(text_POS)
    inf_adj = check_adv_inflectional_adj_row(text_POS)

    all_words = set()

    all_words.update(assim)
    all_words.update(adv_suf)
    all_words.update(compound_words)
    all_words.update(inf_verb)
    all_words.update(inf_adj)

    all_words = list(all_words)
    
    return all_words, num_words


def get_hard_words(snippet, simplify=True):
    
    hard_words, num_words_snippet = calculate(snippet, simplify)
    num_hard_words = len(hard_words)
    if num_words_snippet > 0:
        proportion_hard_words = num_hard_words / num_words_snippet
    else:
        proportion_hard_words = 0
    return hard_words, num_hard_words, proportion_hard_words


def get_hard_words_from_list(snippets, simplify=True):
    proportions_of_hard_words = []
    nums_hard_words = []
    
    for snippet in snippets:
        hard_words, num_hard_words, proportion_hard_words = get_hard_words(snippet, simplify)
        proportions_of_hard_words.append(proportion_hard_words)
        nums_hard_words.append(num_hard_words)
    return proportions_of_hard_words, nums_hard_words

import concurrent.futures
from functools import partial

def get_hard_words_parallel(snippets):
    proportions_of_hard_words = []
    nums_hard_words = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(get_hard_words, snippets))

    for hard_words, num_hard_words, proportion_hard_words in results:
        proportions_of_hard_words.append(proportion_hard_words)
        nums_hard_words.append(num_hard_words)

    return proportions_of_hard_words, nums_hard_words


def get_hard_words_from_file(file_path):
    proportions_of_hard_words = []
    nums_hard_words = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            hard_words, num_hard_words, proportion_hard_words = get_hard_words(line)
            proportions_of_hard_words.append(proportion_hard_words)
            nums_hard_words.append(num_hard_words)
            
    return proportions_of_hard_words, nums_hard_words

