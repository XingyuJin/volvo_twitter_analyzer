import numpy as np
import pandas as pd
from wordcloud import WordCloud, STOPWORDS

from dao.mysql_processor import read_mysql

ori_tweet = read_mysql("twitter_data.`volvo0701-1101`")
volvo_account = read_mysql("twitter_data.volvocarusa_account")

st_words = set(STOPWORDS)
# enhancing stopword by removing @mentions and shorthands
st_words.update(
    ['https', 'CO', 'RT', 'Please', 'via', 'amp', 'place', 'new', 'ttot', 'best', 'great', 'top', 'ht', 'Volvo',
     'car', 'cars'])


def get_follower_num():
    return volvo_account.sort_values("Tweet_time", ascending=False)["Tweet_user_follower"][0]


def get_following_num():
    return volvo_account.sort_values("Tweet_time", ascending=False)["Tweet_user_following"][0]


def get_tweets_num():
    return len(volvo_account)


def get_likes_num():
    return sum(volvo_account["Tweet_like_count"])


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


def get_latest_mention(top_type):
    if top_type == "top_like":
        top = ori_tweet[['Tweet_content', 'Tweet_username', 'Tweet_like_count']].sort_values('Tweet_like_count',
                                                                                             ascending=False).head(5)
    elif top_type == "top_retweet":
        top = ori_tweet[['Tweet_content', 'Tweet_username', 'Tweet_retweet_count']].sort_values('Tweet_retweet_count',
                                                                                                ascending=False).head(5)
    elif top_type == "top_influence":
        count = ori_tweet['Tweet_username'].value_counts()
        df_count = pd.DataFrame()
        df_count['Tweet_username'] = count.index
        df_count['count'] = count.values
        df_count["score"] = df_count["count"] / max(df_count["count"]) * 50
        score_dict = df_count[["Tweet_username", "score"]].set_index('Tweet_username')["score"].to_dict()

        df_userfollower = ori_tweet.loc[:, ['Tweet_username', 'Tweet_user_followers']]
        df_userfollower.sort_values(by='Tweet_user_followers', ascending=False, inplace=True)
        df_userfollower.drop_duplicates(subset='Tweet_username', keep='first', inplace=True)
        df_userfollower["score"] = df_userfollower["Tweet_user_followers"] / max(
            df_userfollower["Tweet_user_followers"]) * 50

        for k, v in df_userfollower[["Tweet_username", "score"]].set_index('Tweet_username')["score"].to_dict().items():
            if k in score_dict:
                score_dict[k] += v

        top = pd.DataFrame(list(score_dict.items()), columns=["Tweet_username", "Tweet_content"], dtype="str").head(5)
    else:
        top = ori_tweet[["Tweet_time", "Tweet_username", "Tweet_content"]].sort_values("Tweet_time",
                                                                                       ascending=False).head(5)

    return top[["Tweet_username", "Tweet_content"]].values


def get_word_cloud():
    wc = WordCloud(height=300, repeat=False, width=500, max_words=50, stopwords=st_words, colormap='terrain',
                   background_color='white').generate(' '.join(ori_tweet['Tweet_content'].dropna().astype(str)))
    return wc.words_
