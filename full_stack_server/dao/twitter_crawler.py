import csv
import json
import os
import re
import time
from urllib.parse import quote, urlencode

import numpy as np
import pandas as pd
import requests
import sklearn
import urllib3
from requests.exceptions import RequestException
from textblob import TextBlob


class WebCrawler:
    def __init__(self, outfile):
        self.csv_filename = outfile
        self.count = 0

    def crawl(self, page):
        raise AssertionError("This is an abstract class and should not be used for crawling")

    @staticmethod
    def init_detail(tweet_id, user_id, content, retweet_id):
        return {
            'Tweet_url': ' ',
            'Tweet_id': tweet_id + '\t',
            'Tweet_user_id': user_id + '\t',
            'Tweet_username': ' ',
            'Tweet_account': ' ',
            'Tweet_user_location': ' ',
            'Tweet_user_followers': ' ',
            'Tweet_user_following': ' ',
            'Tweet_time': ' ',
            'Tweet_location': ' ',
            'Tweet_country_code': ' ',
            'Tweet_content': re.sub(r'https?://.*?\s', ' ',
                                    content.get('full_text').replace('\n', '\t') + ' ').strip(),
            'Tweet_contain_links': ', '.join(
                re.findall(r'(https?://.*?)\s', content.get('full_text').replace('\n', '\t') + ' ')),
            'Tweet_image_urls': ' ',
            'Tweet_retweet_count': content.get('retweet_count'),
            'Tweet_reply_count': content.get('reply_count'),
            'Tweet_like_count': content.get('favorite_count'),
            'Tweet_quote_links': ' ',
            'Retweet_url': ' ',
            'Retweet_id': retweet_id + '\t',
            'Retweet_username': ' ',
            'Retweet_account': ' ',
            'Retweet_time': ' ',
            'Retweet_location': ' ',
            'Retweet_content': ' ',
            'Retweet_contain_links': ' ',
            'Retweet_image_urls': ' '
        }

    @staticmethod
    def parse_date(created_at):
        raw_date = created_at.replace('Jan', '01').replace('Feb', '02').replace('Mar', '03').replace('Apr',
                                                                                                     '04').replace(
            'May', '05').replace('Jun', '06').replace('Jul', '07').replace('Aug', '08') \
            .replace('Sep', '09').replace('Oct', '10').replace('Nov', '11').replace('Dec', '12')

        matching = re.search(r'(\d{2}) (\d{2}) (\d+:\d+:\d+) \+\d{4} (\d{4})', raw_date)
        if matching:
            date = matching.group(4) + '-' + matching.group(1) + '-' + matching.group(2) + ' ' + matching.group(3)
            return date

    def parse_and_save_detail(self, tweets, users):
        quoted_id_list = []
        for tweet_id, content in tweets.items():
            quoted_id = content.get('quoted_status_id_str')
            if quoted_id:
                quoted_id_list.append(quoted_id)

        detail_list = []
        for tweet_id, content in tweets.items():
            retweet_id = content.get('quoted_status_id_str', '')
            user_id = content.get('user_id_str')

            detail = self.init_detail(tweet_id, user_id, content, retweet_id)

            # user_info
            if user_id:
                detail['Tweet_username'] = users.get(user_id).get('name')
                detail['Tweet_account'] = users.get(user_id).get('screen_name')
                detail['Tweet_user_location'] = users.get(user_id).get('location')
                detail['Tweet_user_following'] = users.get(user_id).get('friends_count')
                detail['Tweet_user_followers'] = users.get(user_id).get('followers_count')
                detail['Tweet_url'] = f'https://twitter.com/{detail["Tweet_account"]}/status/{tweet_id}'

            # time
            detail['Tweet_time'] = self.parse_date(content.get('created_at'))

            # location
            if content.get('place'):
                detail['Tweet_location'] = content.get('place').get('full_name')
                detail['Tweet_country_code'] = content.get('place').get('country_code')

            # if image
            entities = content.get('entities')
            if entities:
                media = entities.get('media')
                if media:
                    detail['Tweet_image_urls'] = media[0].get('media_url_https', ' ')

                urls = entities.get('urls')
                if urls:
                    detail['Tweet_quote_links'] = urls[0].get('expanded_url') or urls[0].get('display_url')

            # retweet
            if retweet_id:
                retweet_content = tweets.get(retweet_id)
                if retweet_content:
                    retweet_user_id = retweet_content.get('user_id_str')
                    detail['Retweet_username'] = users.get(retweet_user_id).get('name')
                    detail['Retweet_account'] = users.get(retweet_user_id).get('screen_name')

                    detail['Retweet_time'] = self.parse_date(retweet_content.get('created_at'))

                    if retweet_content.get('place'):
                        detail['Retweet_location'] = retweet_content.get('place').get('full_name', ' ')

                    detail['Retweet_content'] = re.sub(r'https?://.*?\s', ' ',
                                                       retweet_content.get('full_text').replace('\n',
                                                                                                '\t') + ' ').strip()
                    detail['Retweet_contain_links'] = ', '.join(
                        re.findall(r'(https?://.*?)\s', retweet_content.get('full_text').replace('\n', '\t') + ' '))

                    if detail['Retweet_account']:
                        detail['Retweet_url'] = f'https://twitter.com/{detail["Retweet_account"]}/status/{retweet_id}'

                    entities = retweet_content.get('entities')
                    if entities:
                        media = entities.get('media')
                        if media:
                            detail['Retweet_image_urls'] = media[0].get('media_url_https', ' ')

            detail_list.append({tweet_id: detail})

        if quoted_id_list:
            for quoted_id in quoted_id_list:
                for each in detail_list:
                    if quoted_id in each:
                        detail_list.remove(each)

        for detail in detail_list:
            for value in detail.values():
                # print(value)
                self.save(value)

    def save(self, detail):
        if detail:
            if not os.path.exists(self.csv_filename):
                with open(self.csv_filename, 'a', encoding='utf-8-sig', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=list(detail.keys()))
                    writer.writeheader()
                    writer.writerow(detail)
            else:
                with open(self.csv_filename, 'a', encoding='utf-8-sig', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=list(detail.keys()))
                    writer.writerow(detail)

            print(detail)

            self.count += 1

    def run(self):
        page = 1
        while True:
            cursor = self.crawl(page)
            if cursor:
                if cursor != self.current_cursor:
                    self.current_cursor = cursor
                    # time.sleep(1)
                    page += 1
                else:

                    break
            else:
                break


class Twitter(WebCrawler):
    def __init__(self, outfile):
        super().__init__(outfile)
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'cache-control': 'no-cache',
            'Cookie': 'personalization_id="v1_sfs7Hmc754bLJF9mLIK2+g=="; tfw_exp=0; guest_id=v1%3A160185784161918610; _ga=GA1.2.634244249.1601857844; dnt=1; ads_prefs="HBISAAA="; kdt=eMkL34tJfk1PiTvHo4dd8ygie7xuOI9l0XERP53M; _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCNTyKvZ0AToMY3NyZl9p%250AZCIlYWY2ODgxNDMxYzhjY2Y1YzcxOTc0Nzk4ZjQzNjdmN2U6B2lkIiVjYmZk%250AOWYyOTVhYWUzMWI4Y2FiOGE5M2NiY2M3MWEwNToJdXNlcmwrCQCwFYRCaJ4O--f9314ba074a59c3031a09423f6e8c0c929a0e936; des_opt_in=Y; external_referer=padhuUp37zgIPFFJ%2F%2BwGHSs9bDtnY3elTmanMNkwtWc%3D|0|8e8t2xd8A2w%3D; remember_checked_on=1; auth_token=592d84e00ece02cd847adb9ea8793375a838ec0e; twid=u%3D1053393997744418816; ct0=47ce460bc8877b8c1774afceac09a705bd2ba873f880a8730091f9edd9c83f72f4b7bd1438e18229ecb454ccc123896d7c27bb1e9f8bd16b70c4b9c1f0a8339995c4ed7d269ce95086c32d3f20b8b99f; _gid=GA1.2.624236461.1602141514',
            'origin': 'https://twitter.com',
            'pragma': 'no-cache',
            'referer': 'https://twitter.com/search?q=(%23BlackLivesMatter%20OR%20%23GeorgeFloyd)%20until%3A2020-06-02%20since%3A2020-05-25&src=recent_search_click&f=live',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'x-csrf-token': '47ce460bc8877b8c1774afceac09a705bd2ba873f880a8730091f9edd9c83f72f4b7bd1438e18229ecb454ccc123896d7c27bb1e9f8bd16b70c4b9c1f0a8339995c4ed7d269ce95086c32d3f20b8b99f',
            'x-twitter-active-user': 'yes',
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-client-language': 'en',
        }

        urllib3.disable_warnings()

        self.current_cursor = ''

        keyword_list_OR = ['volvo', 'volvoc30', 'volvos60', 'volvoxc40bev', 'volvoxc90', 'volvoxc40', 'volvoxc60',
                           'c30''xc40bev', 'xc40', 'xc90', 's60', 'xc60']

        self.keywords_or = ' OR '.join(keyword_list_OR)

        self.since = '2020-06-01'  # begin
        self.until = '2020-12-01'  # end

        # self.csv_filename = 'volvo0501-1101.csv'

    def crawl(self, page):
        while True:
            q = quote(f'({self.keywords_or}) lang:en until:{self.until} since:{self.since}', safe='()')

            query = {
                'include_profile_interstitial_type': 1,
                'include_blocking': 1,
                'include_blocked_by': 1,
                'include_followed_by': 1,
                'include_want_retweets': 1,
                'include_mute_edge': 1,
                'include_can_dm': 1,
                'include_can_media_tag': 1,
                'skip_status': 1,
                'cards_platform': 'Web-12',
                'include_cards': 1,
                'include_ext_alt_text': 'true',
                'include_quote_count': 'true',
                'include_reply_count': 1,
                'tweet_mode': 'extended',
                'include_entities': 'true',
                'include_user_entities': 'true',
                'include_ext_media_color': 'true',
                'include_ext_media_availability': 'true',
                'send_error_codes': 'true',
                'simple_quoted_tweet': 'true',
                'tweet_search_mode': 'live',
                'count': 20,
                'query_source': 'recent_search_click',
                'pc': 1,
                'spelling_corrections': 1,
                'ext': 'mediaStats,highlightedLabel'
            }

            if page == 1:
                url = 'https://api.twitter.com/2/search/adaptive.json?' + urlencode(query) + f'&q={q}'
            else:
                url = 'https://api.twitter.com/2/search/adaptive.json?' + urlencode(
                    query) + f'&q={q}&cursor={self.current_cursor}'

            try:
                # print(url)
                response = requests.get(url, headers=self.headers, verify=False, timeout=6)

                if response.status_code == 200:
                    datas = response.json()
                    tweets = datas.get('globalObjects').get('tweets')
                    users = datas.get('globalObjects').get('users')

                    if tweets:
                        self.parse_and_save_detail(tweets, users)

                        try:
                            if page == 1:
                                cursor_value = \
                                    datas.get('timeline').get('instructions')[0].get('addEntries').get('entries')[
                                        -1].get('content').get('operation').get('cursor').get('value')
                            else:
                                cursor_value = datas.get('timeline').get('instructions')[-1].get('replaceEntry').get(
                                    'entry').get('content').get('operation').get('cursor').get('value')
                        except AttributeError:
                            return None

                        else:
                            if cursor_value:
                                cursor = quote(cursor_value)
                                return cursor
                            else:
                                return None

                    else:
                        return None

                else:
                    time.sleep(1)
                    continue

            except RequestException as _:
                time.sleep(1)
                continue
            except json.decoder.JSONDecodeError as _:
                time.sleep(1)
                continue


class VolvoAccount(WebCrawler):
    def __init__(self, outfile):
        super().__init__(outfile)
        self.headers = {
            'authority': 'twitter.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'x-twitter-client-language': 'en',
            'x-csrf-token': '47ce460bc8877b8c1774afceac09a705bd2ba873f880a8730091f9edd9c83f72f4b7bd1438e18229ecb454ccc123896d7c27bb1e9f8bd16b70c4b9c1f0a8339995c4ed7d269ce95086c32d3f20b8b99f',
            # 需替换
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-active-user': 'yes',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            # 'referer': 'https://twitter.com/search?q=%23PokemonforHK&src=recent_search_click&f=live',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'personalization_id="v1_sfs7Hmc754bLJF9mLIK2+g=="; tfw_exp=0; guest_id=v1%3A160185784161918610; _ga=GA1.2.634244249.1601857844; dnt=1; ads_prefs="HBISAAA="; kdt=eMkL34tJfk1PiTvHo4dd8ygie7xuOI9l0XERP53M; _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCNTyKvZ0AToMY3NyZl9p%250AZCIlYWY2ODgxNDMxYzhjY2Y1YzcxOTc0Nzk4ZjQzNjdmN2U6B2lkIiVjYmZk%250AOWYyOTVhYWUzMWI4Y2FiOGE5M2NiY2M3MWEwNToJdXNlcmwrCQCwFYRCaJ4O--f9314ba074a59c3031a09423f6e8c0c929a0e936; des_opt_in=Y; external_referer=padhuUp37zgIPFFJ%2F%2BwGHSs9bDtnY3elTmanMNkwtWc%3D|0|8e8t2xd8A2w%3D; remember_checked_on=1; auth_token=592d84e00ece02cd847adb9ea8793375a838ec0e; twid=u%3D1053393997744418816; ct0=47ce460bc8877b8c1774afceac09a705bd2ba873f880a8730091f9edd9c83f72f4b7bd1438e18229ecb454ccc123896d7c27bb1e9f8bd16b70c4b9c1f0a8339995c4ed7d269ce95086c32d3f20b8b99f; _gid=GA1.2.624236461.1602141514'
        }

        self.count = 0

        urllib3.disable_warnings()

        self.current_cursor = ''

        # self.csv_filename = 'VolvoCarUSA.csv'
        # self.keyword = 'volvo'
        self.since = '2019-11-01'
        self.until = '2020-11-01'
        self.account = 'VolvoCarUSA'

    def crawl(self, page):
        while True:
            q = quote(f'(from:{self.account}) lang:en until:{self.until} since:{self.since}', safe='()')

            query = {
                'include_profile_interstitial_type': 1,
                'include_blocking': 1,
                'include_blocked_by': 1,
                'include_followed_by': 1,
                'include_want_retweets': 1,
                'include_mute_edge': 1,
                'include_can_dm': 1,
                'include_can_media_tag': 1,
                'skip_status': 1,
                'cards_platform': 'Web-12',
                'include_cards': 1,
                'include_ext_alt_text': 'true',
                'include_quote_count': 'true',
                'include_reply_count': 1,
                'tweet_mode': 'extended',
                'include_entities': 'true',
                'include_user_entities': 'true',
                'include_ext_media_color': 'true',
                'include_ext_media_availability': 'true',
                'send_error_codes': 'true',
                'simple_quoted_tweet': 'true',
                'tweet_search_mode': 'live',
                'count': 20,
                'query_source': 'recent_search_click',
                'pc': 1,
                'spelling_corrections': 1,
                'ext': 'mediaStats,highlightedLabel'
            }

            if page == 1:
                url = 'https://api.twitter.com/2/search/adaptive.json?' + urlencode(query) + f'&q={q}'
            else:
                url = 'https://api.twitter.com/2/search/adaptive.json?' + urlencode(
                    query) + f'&q={q}&cursor={self.current_cursor}'

            try:
                # print(url)
                response = requests.get(url, headers=self.headers, verify=False, timeout=6)

                if response.status_code == 200:
                    datas = response.json()
                    tweets = datas.get('globalObjects').get('tweets')
                    users = datas.get('globalObjects').get('users')

                    if tweets:
                        self.parse_and_save_detail(tweets, users)

                        try:
                            if page == 1:
                                cursor_value = \
                                    datas.get('timeline').get('instructions')[0].get('addEntries').get('entries')[
                                        -1].get('content').get('operation').get('cursor').get('value')
                            else:
                                cursor_value = datas.get('timeline').get('instructions')[-1].get('replaceEntry').get(
                                    'entry').get('content').get('operation').get('cursor').get('value')
                        except AttributeError:
                            return None

                        else:
                            if cursor_value:
                                cursor = quote(cursor_value)
                                return cursor
                            else:
                                return None

                    else:
                        return None

                else:
                    time.sleep(1)
                    continue

            except RequestException as _:
                time.sleep(1)
                continue
            except json.decoder.JSONDecodeError as _:
                time.sleep(1)
                continue


def preprocess(csv_name):
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


if __name__ == '__main__':
    tw = Twitter("tmp.csv")
    tw.run()
