import numpy as np
import pandas as pd
import sklearn
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS

from dao.mysql_processor import read_mysql

ori_tweet = read_mysql("twitter_data.`volvo0701-1101`")
ori_tweet["Tweet_time"] = pd.to_datetime(ori_tweet["Tweet_time"])
st_words = set(STOPWORDS)

# enhancing stopword by removing @mentions and shorthands
st_words.update(
    ['https', 'CO', 'RT', 'Please', 'via', 'amp', 'place', 'new', 'ttot', 'best', 'great', 'top', 'ht', 'Volvo',
     'car', 'cars'])


def pre_process(csv_name):
    tweet = pd.read_csv(csv_name, error_bad_lines=False)
    tweet = tweet.replace(' ', np.nan)
    tweet = tweet[tweet['Tweet_content'].str.lower().str.contains('volvo|c30|s60|xc40bev|xc90|xc40|xc60|c30|s60')]
    tweet["Tweet_time"] = pd.to_datetime(tweet["Tweet_time"])

    twt_scores = []
    for c in tweet["Tweet_content"]:
        twt_scores.append(TextBlob(c).sentiment.polarity)

    twt_scores = sklearn.preprocessing.minmax_scale(twt_scores, feature_range=(0, 100), axis=0, copy=True)
    tweet["sentiment_score"] = twt_scores
    tweet.to_csv(csv_name)


def get_follower_num():
    return 132


def get_following_num():
    return 41234


def get_tweets_num():
    return len(ori_tweet)


def get_likes_num():
    return 99


def get_region_dist():
    t1 = ori_tweet[~ori_tweet['Tweet_username'].str.contains('volvo|Volvo')]
    t1 = t1[~t1['Tweet_country_code'].isnull()]
    loc = t1['Tweet_country_code'].value_counts() / len(t1)

    other_val = sum(loc[4:])
    loc = loc[:4].to_dict()
    loc["OTHER"] = other_val

    return loc


def get_action_count(action_type, duration_mode):
    if action_type == 0:
        return {"M": 1, "T": 12, "W": 123, "Th": 1234, "F": 15}

    if action_type == 1:
        return {"M": 1, "T": 12, "W": 123, "Th": 1234, "F": 15}

    if action_type == 2:
        return {"M": 1, "T": 12, "W": 123, "Th": 1234, "F": 15}

    if action_type == 3:
        return {"M": 1, "T": 12, "W": 123, "Th": 1234, "F": 15}


def get_model_score():
    car_model = ["s60", "t6", "xc90", "xc60", "xc40"]
    bins = [0, 5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105]
    model_score = {}

    contents = ori_tweet["Tweet_content"].str.lower()
    ori_score = ori_tweet["sentiment_score"]

    for model in car_model:
        scores = ori_score[contents.str.contains(model, regex=False, na=False)]
        model_score[model] = np.histogram(scores, bins)[0]

    return model_score


def get_score_dist():
    positive = round(sum(ori_tweet["sentiment_score"] > 50) / len(ori_tweet), 2)
    neutral = round(sum(np.isclose(ori_tweet["sentiment_score"], 50)) / len(ori_tweet), 2)
    negative = round(sum(ori_tweet["sentiment_score"] < 50) / len(ori_tweet), 2)

    return {"positive": positive, "neutral": neutral, "negative": negative}


def get_avg_score():
    tweet_df_1D = ori_tweet[["Tweet_time", "sentiment_score"]].groupby(
        pd.Grouper(key='Tweet_time', freq='1D', convention='start')).mean()
    return np.round(tweet_df_1D["sentiment_score"], 2)


def get_latest_mention():
    latest = ori_tweet[["Tweet_time", "Tweet_username", "Tweet_content"]].sort_values("Tweet_time",
                                                                                      ascending=False).head(5)
    return latest[["Tweet_username", "Tweet_content"]].values


def get_word_cloud():
    wc = WordCloud(height=300, repeat=False, width=500, max_words=50, stopwords=st_words, colormap='terrain',
                   background_color='white').generate(' '.join(ori_tweet['Tweet_content'].dropna().astype(str)))
    return wc.words_
