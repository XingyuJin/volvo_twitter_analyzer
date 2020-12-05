from google.protobuf.json_format import MessageToJson

import pbgen.view_pb2 as viewpb
from dao import twitter_processor


def get_account_response(duration_mode):
    data = twitter_processor.get_data(duration_mode)
    account_page_resp = viewpb.AccountPageResponse()

    get_account_summary(account_page_resp.summary_resp)

    get_new_action_count(account_page_resp.new_comment_count, 0, data)
    get_new_action_count(account_page_resp.new_like_count, 1, data)
    get_new_action_count(account_page_resp.new_follower_count, 2, data)
    get_new_action_count(account_page_resp.new_mention_count, 3, data)

    get_region_dist_list(account_page_resp.region_dist_list)

    return MessageToJson(account_page_resp, preserving_proto_field_name=True)


def get_account_summary(message):
    message.followers = twitter_processor.get_follower_num()
    message.following = twitter_processor.get_following_num()
    message.tweets = twitter_processor.get_tweets_num()
    message.likes = twitter_processor.get_likes_num()


def get_new_action_count(message, mode, df):
    action_count_dict = twitter_processor.get_action_count(mode, df)
    for k, v in action_count_dict.items():
        action_count = message.add()
        action_count.time = k
        action_count.count = v


def get_region_dist_list(message):
    country_dist_dict = twitter_processor.get_region_dist()

    for k, v in country_dist_dict.items():
        country_dist = message.add()
        country_dist.country_code = k
        country_dist.percentage = round(v, 2)
