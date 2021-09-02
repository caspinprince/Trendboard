# Trendboard

Trendboard is a web-based dashboard that analyzes trends in data from social media APIs.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info

The current version of Trendboard can be viewed and tested [here.](https://media-dashboard.matthewzhang8.repl.co/) 

The webapp is split into two sections with different features:
### Youtube Features:
* Analyze various data about currently trending Youtube videos using different plots.
* Display the most commonly tagged topics in Youtube trends.

### Twitter Features:
* Search for a topic or hashtag and get the average sentiment of recent tweets with that label.
* Display the top trending twitter topics and hashtags by country. 

## Highlights
* **ML Model**
  * The sentiment classifier model training was done on 1.6 million tweets from 
    [kaggle](https://www.kaggle.com/kazanova/sentiment140/code) and the process can be seen in the 
    [twitter_sentiment_analysis_model.ipynb](https://github.com/caspinprince/Trendboard/blob/main/assets/twitter_sentiment_analysis_model.ipynb)
    file under the assets folder.
  * The final model and preprocessor is saved in the [utilities folder](https://github.com/caspinprince/Trendboard/tree/main/utilities)
    
## Setup

If you wish to run the project locally take the following steps:

1. Clone the repository.
2. Create the necessary API keys:
    1. [Youtube Data API](https://developers.google.com/youtube/v3/getting-started)
    2. [Twitter API v1.1](https://developer.twitter.com/en/apply-for-access)
    
3. Under the main folder path create a file named `.env` and insert the API keys in the following format:
```python
YOUTUBEAPIKEY = '<insert youtube api key here>'
TWITTERAPIKEY = '<insert twitter api key here'
TWITTERAPISECRETKEY = '<insert twitter secret key here>'
```
4. Download the necessary packages using `pip install` or `conda install` if using an Anaconda environment (recommended).
5. Run `index.py`!

**Note:** If getting errors related to the **TextCleaner** or **finalTwitterModel**, try deleting 
`finalTwitterModel.pkl` and rerunning model_save.py (this may take some time depending on hardware).

