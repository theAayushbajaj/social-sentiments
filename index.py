from flask import Flask, render_template, request
from rake_nltk import Rake
from tweepy import OAuthHandler
import score_texts_emojis_v5
import json
import hashcode
import pandas as pd

import tensorflow
app = Flask(__name__)

ckey = "2LEQlbO3IkdJ4osG5ZzxHvOAX"
csecret = "4Vijxfwyak5acGNc6Eowu2BvWZ2VbzH3JoFUURFAd5jaSoIsom"
atoken = "846386128278208512-K0NeuaqZ3lXz2NOxH6jH9JRsjG42sC2"
asecret = "4pNF7Eru28tGFaOYISrGkPcTf8ePr0h8s0LTFIh0Fcg0q"

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

r = Rake()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main' , methods=['GET'])
def main():
    keyword = request.args.get('keyword')
    happy_buffer,sad_buffer,fear_buffer,love_buffer,angry_buffer,happy_phrases,sad_phrases,fear_phrases,love_phrases,angry_phrases,happy_location,sad_location,fear_location,love_location,angry_location,top_keywords = score_texts_emojis_v5.start(r , auth , keyword , 500)         
    #print("Sad Location : " , sad_location)
    happy_hash,sad_hash,fear_hash,angry_hash,love_hash = hashcode.hash_function(happy_location,sad_location,fear_location,love_location,angry_location)
    #print(sad_hash)
    '''pd.DataFrame(happy_hash.items()).to_csv('templates/happy.csv', encoding='utf-8')
    pd.DataFrame(sad_hash.items()).to_csv('templates/sad.csv', encoding='utf-8')
    pd.DataFrame(fear_hash.items()).to_csv('templates/fear.csv', encoding='utf-8')
    pd.DataFrame(angry_hash.items()).to_csv('templates/angry.csv', encoding='utf-8')
    pd.DataFrame(love_hash.items()).to_csv('templates/love.csv', encoding='utf-8')'''

    #top_keywords = rake_demo.start(r , auth , keyword , 1000)
    #output = {'happy_buffer':happy_buffer,'sad_buffer':sad_buffer ,'fear_buffer':fear_buffer,'angry_buffer':angry_buffer,'love_buffer':love_buffer, 'keyword' : keyword ,'total_happy':len(happy_buffer),'total_sad':len(sad_buffer),'total_fear':len(fear_buffer),'total_love':len(love_buffer),'total_angry':len(love_buffer), 'top_keywords' : top_keywords}
    #output = json.dumps(output)
    return render_template('main.html' , happy_buffer=happy_buffer,sad_buffer=sad_buffer,fear_buffer=fear_buffer,love_buffer=love_buffer,angry_buffer=angry_buffer, keyword=keyword ,total_happy=len(happy_buffer),total_sad=len(sad_buffer),total_fear=len(fear_buffer),total_love=len(love_buffer),total_angry=len(angry_buffer),happy_phrases=happy_phrases,sad_phrases=sad_phrases,fear_phrases=fear_phrases,love_phrases=love_phrases,angry_phrases=angry_phrases,top_keywords=top_keywords)

if __name__ == '__main__':
    app.run(threaded=False)
