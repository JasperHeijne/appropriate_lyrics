# Recommending Appropriate Lyrics to Youngsters

**Understanding the Presence of Inappropriate Content in Music Lyrics: Insights for Children’s Recommender Systems**

A research project by Jasper Heijne.

## Overview

This research project aims to analyze the presence of inappropriate content in music lyrics and provide insights for developing children’s music recommender systems. The research paper can be found at: (link to TU Delft paper-repository).

### Preprocessing Data

To process the lyrics, use the functions in `processingData.py`.

### Curse Words

- **Get Percentage of Songs with Curse Words**: `googles_curse_words_copy.mjs`
- **Get Percentage of Curse Words per Song**: `googles_curse_words.mjs`
- **Create Boxplot for Curse Words**: `create_curse_word_boxplot.py`

### Profanity

- **Run Profanity Model and Create Boxplot**: `profanity_check_scan.py`

### Offensive Speech

- **Run Offensive Speech Model and Create Boxplot**: `offensive_speech_scan.py`

### Hate Speech

- **Run Hate Speech Model and Create Boxplot**: `hate_speech_scan.py`

### General Functions

- **Write Boxplot Info to File**: `general_functions.py`

### Readability Check

- **Run Readability Methods and Create Boxplot**: `readability_check.py`

### Statistical Analysis

- **Kruskal-Wallis Experiment and Post Hoc Test by Dunn**: `kruskal_willis_dunns.py`

## Discussion

The analysis reveals that inappropriate content is present across various music genres. Recommender systems should be cautious when suggesting Rap and R&B music to children. A more nuanced filter considering different facets of inappropriateness is recommended.

## How to Cite

If you use this code or data in your research, please cite the corresponding publication: (link to TU Delft paper-repository).

