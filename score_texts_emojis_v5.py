# -*- coding: utf-8 -*-

""" Use DeepMoji to score texts for emoji distribution.

The resulting emoji ids (0-63) correspond to the mapping
in emoji_overview.png file at the root of the DeepMoji repo.

Writes the result to a csv file.
"""
from __future__ import print_function, division
import json
import csv
import numpy as np
from deepmoji.sentence_tokenizer import SentenceTokenizer
from deepmoji.model_def import deepmoji_emojis
from deepmoji.global_variables import PRETRAINED_PATH, VOCAB_PATH
from tweepy import OAuthHandler
import tweepy
import re

class_tokens = {'happy': [4, 6, 7, 10, 11, 15, 16, 17, 28, 23, 31, 33, 48, 50, 53, 54],
                'sad': [3, 5, 19, 22, 25, 27, 29, 34, 43, 46],
                'fear': [29, 43, 51, 52], 'angry': [32, 55, 37, 58, 44], 'love': [8, 18, 59, 60, 61, 24, 47]
                }


def start(r, auth, keyword, max_items):
    api = tweepy.API(auth)
    para = ""

    happy_counter = 0;
    sad_counter = 0;
    fear_counter = 0;
    angry_counter = 0;
    love_counter = 0;

    happy_buffer = []
    sad_buffer = []
    fear_buffer = []
    angry_buffer = []
    love_buffer = []

    happy_phrases = []
    sad_phrases = []
    fear_phrases = []
    angry_phrases = []
    love_phrases = []

    happy_para = ''
    sad_para = ''
    fear_para = ''
    angry_para = ''
    love_para = ''

    happy_location = []
    sad_location = []
    fear_location = []
    angry_location = []
    love_location = []

    def check_token(token):
        for i in class_tokens:
            if token in class_tokens[i]:
                return i
        return -1

    TEST_SENTENCES = []

    LOCATIONS = []

    for tweet in tweepy.Cursor(api.search, q=keyword, count=100, lang='en', include_entities=False,
                               tweet_mode='extended').items(max_items):

        location = tweet.user.location
        if not location:
            location = ""
        else:
            if "," in location:
                location = location[0:location.index(",")]

        location = location.strip()
        LOCATIONS.append(location)
        # print('Location :' , location)

        temp = tweet._json.get('full_text')

        if temp.startswith("RT"):
            try:
                temp = tweet._json.get('retweeted_status').get('full_text')
            except:
                temp = tweet._json.get('full_text')
        else:
            temp = tweet._json.get('full_text')

        temp = temp.replace("RT ", "").replace("!", "").replace("..", "").replace("$", "").replace("%", "").replace("&",
                                                                                                                    "").replace(
            "~", "").replace("-", "").replace("+", "").replace("#", "").replace("\\n", "").replace("\\", "").replace(
            "|",
            "")

        temp = " ".join(filter(lambda x: x[0] != '@', temp.split()))
        temp = re.sub(r'https\S+', "", temp)
        temp = temp.strip()
        para = para + temp
        TEST_SENTENCES.append(temp)

    #print('Locations :', LOCATIONS)
    r.extract_keywords_from_text(para)
    # r.get_ranked_phrases_with_scores()

    ranked_phrases = r.get_ranked_phrases()

    for i in range(0, len(ranked_phrases)):
        ranked_phrases[i] = ranked_phrases[i].replace(",", "").replace("'", "").replace("(", "").replace(')',
                                                                                                         "").replace(
            '.', "").replace('`', "").replace('!', "")

        ranked_phrases[i] = re.sub(' +', ' ', ranked_phrases[i]).strip()

    top_keywords = ranked_phrases[:]

    for i in range(0, len(ranked_phrases)):

        t1 = ranked_phrases[i].split()
        if len(t1) > 3:
            top_keywords.remove(ranked_phrases[i])

    # print(TEST_SENTENCES)

    def top_elements(array, k):
        ind = np.argpartition(array, -k)[-k:]
        return ind[np.argsort(array[ind])][::-1]

    maxlen = 30
    batch_size = 32

    # print('Tokenizing using dictionary from {}'.format(VOCAB_PATH))
    with open(VOCAB_PATH, 'r') as f:
        vocabulary = json.load(f)
    st = SentenceTokenizer(vocabulary, maxlen)
    tokenized, _, _ = st.tokenize_sentences(TEST_SENTENCES)

    # print('Loading model from {}.'.format(PRETRAINED_PATH))
    model = deepmoji_emojis(maxlen, PRETRAINED_PATH)
    #model.summary()

    # print('Running predictions.')
    prob = model.predict(tokenized)

    # Find top emojis for each sentence. Emoji ids (0-63)
    # correspond to the mapping in emoji_overview.png
    # at the root of the DeepMoji repo.
    # print('Writing results to {}'.format(OUTPUT_PATH))
    scores = []
    for i, t in enumerate(TEST_SENTENCES):
        t_tokens = tokenized[i]
        t_score = [t]
        t_prob = prob[i]
        ind_top = top_elements(t_prob, 5)
        t_score.append(sum(t_prob[ind_top]))
        t_score.append(ind_top)
        t_score.append([t_prob[ind] for ind in ind_top])
        t_score.append('' + LOCATIONS[i])
        scores.append(t_score)
    # print(t_score)

    # print('Scores skjdvbkjsdbvjk : ' , scores[0])

    for i, row in enumerate(scores):
        try:
            # print(row[0])
            # print('row 2')
            # print(row[2][0])

            # if (row[2] in class_tokens]
            temp = check_token(row[2][0])
            # print(temp)

            if temp == 'sad':
                sad_counter = 1 + sad_counter;
                sad_buffer.append(row[0])
                sad_para = sad_para + row[0]
                sad_location.append(row[4])



            elif temp == 'happy':
                happy_counter = 1 + happy_counter;
                # print("happy counter");
                # print(happy_counter);
                happy_buffer.append(row[0])
                happy_para = happy_para + row[0]
                happy_location.append(row[4])

            elif temp == 'fear':
                fear_counter = 1 + fear_counter;
                fear_buffer.append(row[0])
                fear_para = fear_para + row[0]
                fear_location.append(row[4])


            elif temp == 'angry':
                angry_counter = 1 + angry_counter;
                angry_buffer.append(row[0])
                angry_para = angry_para + row[0]
                angry_location.append(row[4])


            elif temp == 'love':
                love_counter = 1 + love_counter;
                love_buffer.append(row[0])
                love_para = love_para + row[0]
                love_location.append(row[4])

        except Exception:
            pass
        # print("Exception at row {}!".format(i))

    # print("Angry buffer : " , angry_buffer)
    # print("Sad buffer : " , sad_buffer)

    r.extract_keywords_from_text(happy_para)
    happy_phrases = r.get_ranked_phrases()[0:3]

    r.extract_keywords_from_text(sad_para)
    sad_phrases = r.get_ranked_phrases()[0:3]

    r.extract_keywords_from_text(fear_para)
    fear_phrases = r.get_ranked_phrases()[0:3]

    r.extract_keywords_from_text(angry_para)
    angry_phrases = r.get_ranked_phrases()[0:3]

    r.extract_keywords_from_text(love_para)
    love_phrases = r.get_ranked_phrases()[0:3]

    # print("Phrases " , happy_phrases)
    # print("Angry Locations : " , angry_location)

    return happy_buffer, sad_buffer, fear_buffer, love_buffer, angry_buffer, happy_phrases, sad_phrases, fear_phrases, love_phrases, angry_phrases, happy_location, sad_location, fear_location, love_location, angry_location, top_keywords[
                                                                                                                                                                                                                                :10]
