import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import pandas as pd
from wordcloud import WordCloud, STOPWORDS

load_dotenv()
api_key = os.getenv('YOUTUBEAPIKEY')

youtube = build('youtube', 'v3', developerKey=api_key)

def getData(numResults: int):
    request = youtube.videos().list(
        part ='snippet, statistics',
        chart='mostPopular',
        maxResults = numResults,
        regionCode='CA'
    )
    response = request.execute()
    df = pd.json_normalize(response, 'items')
    df = df[['snippet.publishedAt', 'snippet.title',
             'snippet.description', 'snippet.channelTitle',
             'snippet.tags', 'snippet.categoryId',
             'statistics.viewCount', 'statistics.likeCount',
             'statistics.dislikeCount', 'statistics.commentCount']]
    df.columns = ['Publish Date', 'Video Title', 'Description', 'Channel',
                  'Tags', 'Category ID', 'Views', 'Likes', 'Dislikes', 'Comments']
    df['Trending Rank'] = df.index+1
    df = df.convert_dtypes()
    df['Publish Date'] = pd.to_datetime(df['Publish Date'])
    df[['Category ID', 'Views',
        'Likes', 'Dislikes', 'Comments']] = df[['Category ID', 'Views',
                                                'Likes', 'Dislikes', 'Comments']].apply(pd.to_numeric)
    return df

def get_wordcloud(data):
    all_words = ""
    for taglist in data['Tags']:
        if type(taglist) == float:
            continue
        text = set()
        for item in taglist:
            for word in item.split():
                if word.encode().isalnum():
                    text.add(word)
        for x in text:
            all_words += x + " "
    wordcloud = WordCloud(width=1024, height=700, background_color="white", stopwords = set(STOPWORDS)).generate(all_words)
    return wordcloud.to_image()