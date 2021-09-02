import tweepy as tw
import os
from dotenv import load_dotenv
import math
from wordcloud import WordCloud
import joblib
from utilities.model.TextCleaner import TextCleaner

load_dotenv()
consumer_key = os.getenv('TWITTERAPIKEY')
consumer_secret = os.getenv('TWITTERAPISECRETKEY')

auth = tw.OAuthHandler(consumer_key, consumer_secret)
api = tw.API(auth)
model = joblib.load('utilities/model/finalTwitterModel.pkl')

def getTweets(topic, numItems):
    tweets=[]
    for tweet_info in tw.Cursor(api.search, q=topic, lang='en', tweet_mode='extended').items(500):
        if 'retweeted_status' in dir(tweet_info):
            tweets.append(tweet_info.retweeted_status.full_text)
        else:
            tweets.append(tweet_info.full_text)
    predictions = model.predict(tweets)
    print(tweets)
    print(predictions)
    print(f"The topic: {topic} is {100*sum(predictions)/len(tweets)}% positive!")

def getTrendWordcloud(country):
    trendlist = api.trends_place(id=country)
    trendnames = {name['name']:10-math.log(index) for index, name in enumerate(trendlist[0]['trends'], start=1) if name['name'].encode().isascii()}
    wordcloud = WordCloud(width=1024, height=700).generate_from_frequencies(trendnames)
    return wordcloud.to_image()

def getCountries():
    trendavail = api.trends_available()
    return {item['country']:item['woeid'] for item in trendavail if item['placeType']['name'] == 'Country'}

