import numpy as np
import pandas as pd
import sklearn
from textblob import TextBlob

ori_tweet = pd.read_csv("./dao/volvo0701-1101.csv", error_bad_lines=False)
ori_tweet["Tweet_time"] = pd.to_datetime(ori_tweet["Tweet_time"])


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


def get_data(duration_mode=-1):
    return ori_tweet


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


def get_action_count(tweet, mode):
    return {"M": 1, "T": 12, "W": 123, "Th": 1234, "F": 15}


def get_model_score():
    car_model = ["s60", "t6", "xc90", "xc60", "xc40"]
    bins = [0] + list(np.arange(5, 110, 10))
    model_score = {}

    for model in car_model:
        scores = ori_tweet[ori_tweet["Tweet_content"].str.lower().str.contains(model, regex=False, na=False)]["sentiment_score"]
        scores = np.histogram(scores, bins)[0]
        model_score[model] = scores

    return model_score


def get_score_dist():
    positive = round(sum(ori_tweet["sentiment_score"] > 50) / len(ori_tweet), 2)
    neutral = round(sum(np.isclose(ori_tweet["sentiment_score"], 50)) / len(ori_tweet), 2)
    negative = round(sum(ori_tweet["sentiment_score"] < 50) / len(ori_tweet), 2)

    return {"positive": positive, "neutral": neutral, "negative": negative}


def get_avg_score():
    tweet_df_1D = ori_tweet[["Tweet_time", "sentiment_score"]].groupby(
        pd.Grouper(key='Tweet_time', freq='1D', convention='start')).mean()
    return list(np.round(tweet_df_1D["sentiment_score"], 2))


def get_latest_mention():
    latest = ori_tweet[["Tweet_time", "Tweet_username", "Tweet_content"]].sort_values("Tweet_time", ascending=False).head(5)
    return latest[["Tweet_username", "Tweet_content"]].values


def get_word_cloud():
    return {"M": 1, "T": 12, "W": 123, "Th": 1234, "F": 15}
