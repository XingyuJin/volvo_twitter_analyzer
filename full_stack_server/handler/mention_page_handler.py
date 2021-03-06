from google.protobuf.json_format import MessageToJson

import pbgen.view_pb2 as viewpb
from dao import twitter_processor


def get_mention_response():
    mention_page_resp = viewpb.MentionPageResponse()

    get_model_score(mention_page_resp.model_score_list)
    get_score_dist(mention_page_resp.score_dist)
    get_avg_score(mention_page_resp.avg_score)
    get_top_twitter(mention_page_resp.top_twitter)
    get_word_cloud(mention_page_resp.word_cloud)
    get_pred_score(mention_page_resp)
    return MessageToJson(mention_page_resp, including_default_value_fields=True, preserving_proto_field_name=True)


def get_model_score(message):
    model_score_dict = twitter_processor.get_model_score()
    for k, v in model_score_dict.items():
        model_score = message.add()
        model_score.model = k
        model_score.score_dist.extend(v)


def get_score_dist(message):
    score_dist_dict = twitter_processor.get_score_dist()
    message.positive = score_dist_dict["positive"]
    message.negative = score_dist_dict["negative"]
    message.neutral = score_dist_dict["neutral"]


def get_avg_score(message):
    avg_score = twitter_processor.get_avg_score()
    message.extend(avg_score)


def get_pred_score(message):
    pred = twitter_processor.get_pred_result()
    message.future_warning = pred


def get_top_twitter(message):
    for t in ["recent", "top_like", "top_retweet", "top_influence"]:
        top_twitter = message.add()
        top_twitter.type = t

        latest_mention_lst = twitter_processor.get_latest_mention(t)
        for tw in latest_mention_lst:
            latest_mention = top_twitter.twitters.add()
            latest_mention.author = tw[0]
            latest_mention.content = tw[1]


def get_word_cloud(message):
    word_cloud_dict = twitter_processor.get_word_cloud()
    for k, v in word_cloud_dict.items():
        word_cloud = message.add()
        word_cloud.word = k
        word_cloud.count = int(v * 1000)
