# Social Media Sentiment Analysis

This web-app focusses on analyzing sentiments and keyphrase extraction on twitter data from tweepy api and generating a report.

### Overview
* [deepmoji/](deepmoji) contains all the underlying code used to calculate sentiment.
* [templates/](templates) contains the front-end code used for report generation.
* [model/](model) contains the pretrained model and vocabulary.
* [index.py](index.py) contains code to fire up the Flask server.

### Installation
-  Local Machine Installation 
```sh
$ git clone https://github.com/theAayushbajaj/Social-Media-Sentiment-Analysis.git
$ cd Social-Media-Sentiment-Analysis/
$ pip install -r requirements.txt
$ python index.py
```
- Docker Run
```sh
$ sudo docker build -t socialsentiments:latest .
$ docker run --name socialsentiments -v "$(pwd)":/home -p5000:5000 socialsentiments:latest
```
