from google.protobuf.json_format import MessageToJson

import pbgen.view_pb2 as viewpb
from dao import twitter_processor


def get_mention_response():
    data = twitter_processor.get_data()
    mention_page_resp = viewpb.MentionPageResponse()

    get_model_score(mention_page_resp.model_score_list, data)
    get_score_dist(mention_page_resp.score_dist, data)
    get_avg_score(mention_page_resp.avg_score, data)
    get_latest_mention(mention_page_resp.latest_mentions, data)
    get_word_cloud(mention_page_resp.word_cloud, data)

    return MessageToJson(mention_page_resp, preserving_proto_field_name=True)


def get_model_score(message, df):
    model_score_dict = twitter_processor.get_model_score(df)
    for k, v in model_score_dict.items():
        model_score = message.add()
        model_score.model = k
        model_score.score_dist.extend(v)


def get_score_dist(message, df):
    score_dist_dict = twitter_processor.get_score_dist(df)
    message.positive = score_dist_dict["positive"]
    message.negative = score_dist_dict["negative"]
    message.neutral = score_dist_dict["neutral"]


def get_avg_score(message, df):
    avg_score = twitter_processor.get_avg_score(df)
    message.extend(avg_score)


def get_latest_mention(message, df):
    latest_mention_lst = twitter_processor.get_latest_mention(df)
    for tw in latest_mention_lst:
        latest_mention = message.add()
        latest_mention.author = tw[0]
        latest_mention.content = tw[1]


def get_word_cloud(message, df):
    word_cloud_dict = twitter_processor.get_word_cloud(df)
    for k, v in word_cloud_dict.items():
        word_cloud = message.add()
        word_cloud.word = k
        word_cloud.count = v
