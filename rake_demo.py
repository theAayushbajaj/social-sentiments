import tweepy
import re
import nltk


def start(r , auth ,keyword,max_items):

    api = tweepy.API(auth)
    para = ""

    for tweet in tweepy.Cursor(api.search, q=keyword, count=100, lang='en', include_entities=False,
                               tweet_mode='extended').items(max_items):

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
            "~", "").replace("-", "").replace("+", "").replace("#", "").replace("\\n", "").replace("\\", "").replace("|",
                                                                                                                     "")

        temp = " ".join(filter(lambda x: x[0] != '@', temp.split()))
        temp = re.sub(r'https\S+', "", temp)
        temp = temp.strip()
        para = para + temp

    #print(para)

    r.extract_keywords_from_text(para)
    # r.get_ranked_phrases_with_scores()

    ranked_phrases = r.get_ranked_phrases()

  
    for i in range(0, len(ranked_phrases)):
	ranked_phrases[i] = ranked_phrases[i].replace(",", "").replace("'", "").replace("(", "").replace(')', "").replace('.', "").replace('`', "").replace('!', "")

        ranked_phrases[i] = re.sub(' +', ' ', ranked_phrases[i]).strip()

    temp = ranked_phrases[:]

    for i in range(0, len(ranked_phrases)):

        t1 = ranked_phrases[i].split()
        if len(t1) > 3:
            temp.remove(ranked_phrases[i])

    return temp[:10]
