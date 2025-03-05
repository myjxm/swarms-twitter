from twikit import Client, User
from dotenv import load_dotenv
from .sqlexec import *
import trio
from datetime import datetime, timedelta
import twikit
import time

load_dotenv()
cookies = {"auth_token": '6b352a60fc5b02c731f400b7c7a990759012810f',
           "ct0": 'c7689c3118648416c38e051b1ae7aed0311b92f3d935d1515d74eaab1767922057f1130cba27da60be5e99c24701d8b5f5739d8f65f97232476bf88414142598528fb2be7418bed212e0c97a9325567f'}
client = Client('en-US')
client.set_cookies(cookies)


def _addUserInfoToDB(userId: str):
    user = trio.run(lambda: client.get_user_by_id(userId))
    add_tweet_user(user)
    return 'Success to addUserInfoTODB tweet user {0}'.format(userId)


def addUserInfoToDB(userId: str):
    try:
        if not check_user_exist(userId):
            _addUserInfoToDB(userId)
    except Exception as e:
        return 'Failed to add userInfo to DB {0} because:{1}. You can retry directly, modify the parameters and retry, or cancel the operation.'.format(
            userId, e)
    return 'Success to add userInfo to DB tweet user {0}'.format(userId)


def addTweetInfoToDB(tweet: Tweet):
    try:
        trio.run(lambda: client.get_tweet_by_id(tweet.id))
        if not check_tweet_exist(tweet.id):
            add_tweet(tweet, tag='onwer')
    except Exception as e:
        raise
        # return 'Failed to add tweet to DB {0} because:{1}. You can retry directly, modify the parameters and retry, or cancel the operation.'.format(
        #     tweet.id, e)
    return 'Success to add tweet {0} to DB'.format(tweet.id)


def update_db_info():
    users = query_openchain_user()
    for user_id_tag in users:
        user = trio.run(lambda: client.get_user_by_id(user_id_tag[0]))
        update_openchain_user(user, user_id_tag[1])
    tweet_id = query_openchain_tweet()
    for tweet_id_tag in tweet_id:
        tweet = trio.run(lambda: client.get_tweet_by_id(tweet_id_tag[0]))
        update_openchain_tweet(tweet, tweet_id_tag[1])
    update_user_analysis(users)


def twitter_user_analysis(tag, days=7):
    user_analysis = {}
    columns = ['id', 'name', 'description', 'followers_count', 'fast_followers_count', 'most_reply_tweet',
               'most_like_tweet', 'most_view_tweet', 'most_retweet_tweet', 'most_engagements_tweet', 'total_likes',
               'total_replies', 'total_views', 'total_retweets', 'engagement_rate', 'create_date']

    select_user_info = "select a.id,name,description,followers_count,fast_followers_count,most_reply_tweet,most_like_tweet,most_view_tweet,most_retweet_tweet,most_engagements_tweet,total_likes,total_replies,total_views,total_retweets,engagement_rate,b.create_date from tweet_user a inner join user_analysis b on a.id = b.id and a.start_dt = b.create_date where a.start_dt >= date('now', '-" + str(
        days) + " days') and a.tag = '" + str(tag) + "'"
    res = query_sql_exec(select_user_info)
    for row in res:
        user_id = row[0]
        user_info = dict(zip(columns, row))
        user_analysis[user_id] = user_info
    return user_analysis


def twitter_tweet_analysis(tag, days=7):
    tweet_analysis = {}
    columns = ['id', 'create_date', 'userId', 'text', 'in_reply_to', 'quote_count', 'reply_count', 'favorite_count',
               'view_count', 'retweet_count', 'full_text', 'start_dt']
    select_tweet_info = "select id,create_date,userId,text,in_reply_to,quote_count,reply_count,favorite_count,view_count,retweet_count,full_text,start_dt,tag from tweet where start_dt >= date('now', '-" + str(
        days) + " days') and tag = '" + str(tag) + "'"
    res = query_sql_exec(select_tweet_info)
    for row in res:
        tweet_id = row[0]
        tweet_info = dict(zip(columns, row))
        tweet_analysis[tweet_id] = tweet_info
    return tweet_analysis


def update_user_analysis(users):
    for user_id_tag in users:
        user = trio.run(lambda: client.get_user_by_id(user_id_tag[0]))
        res = get_user_analysis(user)
        add_user_analysis(res)


def get_user_analysis(user: User, days=30):
    # 账号分析
    most_reply_tweet = None
    most_like_tweet = None
    most_view_tweet = None
    most_retweet_tweet = None  # retweet+quote
    most_engagements_tweet = None
    total_likes = 0
    total_replies = 0
    total_views = 0
    total_retweets = 0  # retweet+quote
    tweets = trio.run(lambda: user.get_tweets('Tweets', user.statuses_count))
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")
    thirty_days_ago = now - timedelta(days=days)
    tweets_list = []
    while (True):
        for tweet in tweets:
            naive_created_at = tweet.created_at_datetime.replace(tzinfo=None)
            if thirty_days_ago <= naive_created_at <= now:
                tweets_list.append(tweet)
        try:
            # tweets = trio.run(lambda: tweets.next())
            tweets = []
        except twikit.errors.TooManyRequests as e:
            print("Rate limit exceeded, waiting before retry...")
            # 等待指定时间（以秒为单位，可以调整）
            # time.sleep(900)  # 等待 15 分钟（900 秒）
            # tweets = trio.run(lambda: tweets.next())
            tweets = []

        if len(tweets) == 0:
            break;
    for tweet in tweets_list:
        total_likes += tweet.favorite_count
        if tweet.view_count is not None:
            total_views += int(tweet.view_count)
        else:
            total_views += 0
        total_replies += tweet.reply_count
        total_retweets += tweet.retweet_count + tweet.quote_count
        if most_reply_tweet is None:
            most_reply_tweet = tweet
        elif most_reply_tweet.reply_count < tweet.retweet_count:
            most_reply_tweet = tweet
        if most_engagements_tweet is None:
            most_engagements_tweet = tweet
        elif most_engagements_tweet.retweet_count + most_engagements_tweet.reply_count + most_engagements_tweet.quote_count + most_engagements_tweet.favorite_count < tweet.retweet_count + tweet.reply_count + tweet.quote_count + tweet.favorite_count:
            most_engagements_tweet = tweet
        if most_like_tweet is None:
            most_like_tweet = tweet
        elif most_like_tweet.favorite_count < tweet.favorite_count:
            most_like_tweet = tweet
        if tweet.view_count is not None:
            if most_view_tweet is None:
                most_view_tweet = tweet
            elif int(most_view_tweet.view_count) < int(tweet.view_count):
                most_view_tweet = tweet
        if most_retweet_tweet is None:
            most_retweet_tweet = tweet
        elif most_retweet_tweet.retweet_count + most_retweet_tweet.quote_count < tweet.retweet_count + tweet.quote_count:
            most_retweet_tweet = tweet
    engagement_rate = (total_likes + total_replies + total_retweets) / user.followers_count
    analysis_report = {}
    analysis_report['id'] = user.id
    analysis_report['engagement_rate'] = engagement_rate
    analysis_report['total_likes'] = total_likes
    analysis_report['total_replies'] = total_replies
    analysis_report['total_views'] = total_views
    analysis_report['total_retweets'] = total_retweets
    analysis_report['most_reply_tweet'] = most_reply_tweet.id + ":" + most_reply_tweet.text
    analysis_report['most_like_tweet'] = most_like_tweet.id + ":" + most_like_tweet.text
    analysis_report['most_view_tweet'] = most_view_tweet.id + ":" + most_view_tweet.text
    analysis_report['most_retweet_tweet'] = most_retweet_tweet.id + ":" + most_retweet_tweet.text
    analysis_report['most_engagements_tweet'] = most_engagements_tweet.id + ":" + most_engagements_tweet.text
    analysis_report['create_date'] = formatted_date
    return analysis_report


if __name__ == "__main__":
    print(addUserInfoToDB("109065990"))
