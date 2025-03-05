#!/usr/bin/python

import sqlite3
from twikit import user, Tweet
from datetime import datetime

# data=c.execute('''create table tweet_user(
# id varchar(50) primary key not null, -- 'The unique identifier of the user.',
# create_date date not null, -- 'The date and time when the user account was created.',
# name varchar(50) not null, -- 'The user's name.',
# url   varchar(50),  -- 'The user's URL.'
# location varchar(30), -- ' The user's location information.',
# description varchar(100), -- 'The user's profile description.',
# is_blue_verified bool, -- 'Indicates if the user is verified with a blue checkmark.',
# verified bool, --'Indicates if the user is verified.',
# can_dm bool, --'Indicates whether the user can receive direct messages.',
# followers_count int,  -- 'The count of followers.',
# fast_followers_count  int,  -- 'The count of fast followers.',
# normal_followers_count int,  -- 'The count of normal followers.',
# following_count   int,  -- 'The count of users the user is following.',
# dw_snsh_dt  date not null  -- 'Date of statistics'
# )''')

# data=c.execute('''create table tweet_tweet(
#     id  varchar(50) primary key ,--The unique identifier of the tweet.
#     created_date date ,-- The date and time when the tweet was created.
#     created_at_datetime timestamp, --The created_at converted to datetime.
#     user_id  varchar(50), --Author of the tweet.
#     quote_count int,--The count of quotes for the tweet.
#     reply_count int,--The count of replies to the tweet.
#     favorite_count int,--The count of favorites or likes for the tweet.
#     view_count  int,--The count of views.
#     retweet_count int --The count of retweets for the tweet.
# )''')


# create table tweet(
# id text  primary key not null -- 'The unique identifier of the tweet.',
# create_date date not null -- 'The date and time when the tweet was created.',
# userId text not null -- 'Author of the tweet.',
# text  text  --'The full text of the tweet.',
# in_reply_to text --'The tweet ID this tweet is in reply to, if any',
# quote_tweet_id text  --'The Tweet being quoted (if any)',
# quote_count  int --'The count of quotes for the tweet.',
# reply_count   int  --'The count of replies to the tweet.',
# favorite_count   int  --'The count of favorites or likes for the tweet.',
# view_count  int  --'The count of views.',
# retweet_count   int  --'The count of retweets for the tweet.',
# full_text  text  --'The full text of the tweet.',
# dw_snsh_dt  date not null  -- 'Date of statistics',
# tag TEXT default 'competitor' not null)


# data=c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='tweet_user';")
# for row in data:
#    print(row)
#
# data=c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='tweet_tweet';")
# for row in data:
#    print(row)
db_path = '/Users/ddt/Documents/blockchain/smartwarm/swarms-twitter/test.db'


def query_sql_exec(sql, db=db_path):
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        res = c.execute(sql)
        results = res.fetchall()
        conn.commit()
    except Exception as e:
        conn.close()
        raise
    finally:
        conn.close()
    return (results)

def insert_sql_exec(sql, db=db_path):
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        res = c.execute(sql)
        conn.commit()
    except Exception as e:
        conn.close()
        raise
    finally:
        conn.close()
    return res


def add_tweet_user(userinfo: user, tag='competitor'):
    # 获取当前日期
    current_date = datetime.now()
    # 格式化日期为 yyyy - mm - dd 格式
    formatted_date = current_date.strftime("%Y-%m-%d")
    insert_sql = "INSERT INTO tweet_user (id,create_date,name,url,location,description,is_blue_verified,verified,can_dm,followers_count,fast_followers_count,normal_followers_count,following_count,start_dt,tag,end_dt) VALUES ('{0}', '{1}', '{2}','{3}','{4}','{5}',{6},{7},{8},{9},{10},{11},{12},'{13}','{14}','{15}' )".format(
        userinfo.id, userinfo.created_at, userinfo.name, userinfo.url, userinfo.location, userinfo.description,
        userinfo.is_blue_verified, userinfo.verified, userinfo.can_dm, userinfo.followers_count,
        userinfo.fast_followers_count, userinfo.normal_followers_count, userinfo.following_count, formatted_date, tag,
        '9999-12-31')
    try:
        conn = sqlite3.connect('/Users/ddt/Documents/blockchain/smartwarm/swarms-twitter/test.db')
        c = conn.cursor()
        res = c.execute(insert_sql)
        conn.commit()
    except Exception as e:
        conn.close()
        raise
    finally:
        conn.close()
    return 'Success'


def check_user_exist(userid: str) -> bool:
    select_sql = "SELECT * FROM tweet_user where id = '{0}'".format(userid)
    try:
        conn = sqlite3.connect('/Users/ddt/Documents/blockchain/smartwarm/swarms-twitter/test.db')
        c = conn.cursor()
        res = c.execute(select_sql)
        results = res.fetchall()
        conn.commit()
    except Exception as e:
        conn.close()
        raise
    finally:
        conn.close()
    if len(results) > 0:
        return True
    else:
        return False


def query_openchain_user():
    # 获取当前日期
    current_date = datetime.now()
    # 格式化日期为 yyyy - mm - dd 格式
    formatted_date = current_date.strftime("%Y-%m-%d")
    select_sql = "SELECT id,tag FROM tweet_user where end_dt = '9999-12-31' and start_dt < '{0}'".format(formatted_date)
    try:
        conn = sqlite3.connect('/Users/ddt/Documents/blockchain/smartwarm/swarms-twitter/test.db')
        c = conn.cursor()
        res = c.execute(select_sql)
        results = res.fetchall()
        conn.commit()
    except Exception as e:
        print(e)
        conn.close()
        raise
    finally:
        conn.close()
    return results


def update_openchain_user(userinfo: user, tag):
    # 获取当前日期
    current_date = datetime.now()
    # 格式化日期为 yyyy - mm - dd 格式
    formatted_date = current_date.strftime("%Y-%m-%d")
    update_sql = "update tweet_user set end_dt='{0}' where id='{1}' and end_dt='9999-12-31'".format(formatted_date,
                                                                                                    userinfo.id)
    try:
        conn = sqlite3.connect('/Users/ddt/Documents/blockchain/smartwarm/swarms-twitter/test.db')
        c = conn.cursor()
        c.execute(update_sql)
        conn.commit()
    except Exception as e:
        conn.close()
        raise
    finally:
        conn.close()
    add_tweet_user(userinfo, tag)


def add_tweet(tweet: Tweet, tag='onwer'):
    # 获取当前日期
    current_date = datetime.now()
    # 格式化日期为 yyyy - mm - dd 格式
    formatted_date = current_date.strftime("%Y-%m-%d")

    print(formatted_date)
    insert_sql = """
        INSERT INTO tweet (
            id, create_date, userId, text, in_reply_to, quote_count, reply_count, 
            favorite_count, view_count, retweet_count, full_text, start_dt, tag, end_dt
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    values = (tweet.id, tweet.created_at, tweet.user.id, tweet.text, tweet.in_reply_to, tweet.quote_count, tweet.reply_count,
        tweet.favorite_count, 0, tweet.retweet_count, tweet.full_text, formatted_date, tag, '9999-12-31')

    try:
        conn = sqlite3.connect('/Users/ddt/Documents/blockchain/smartwarm/swarms-twitter/test.db')
        c = conn.cursor()
        res = c.execute(insert_sql,values)
        conn.commit()
    except Exception as e:
        conn.close()
        raise
    finally:
        conn.close()
    return 'Success'


def check_tweet_exist(tweetId: str):
    select_sql = "SELECT * FROM tweet where id = '{0}'".format(tweetId)
    try:
        conn = sqlite3.connect('/Users/ddt/Documents/blockchain/smartwarm/swarms-twitter/test.db')
        c = conn.cursor()
        res = c.execute(select_sql)
        results = res.fetchall()
        conn.commit()
    except Exception as e:
        conn.close()
        raise
    finally:
        conn.close()
    if len(results) > 0:
        return True
    else:
        return False


def query_openchain_tweet():
    # 获取当前日期
    current_date = datetime.now()
    # 格式化日期为 yyyy - mm - dd 格式
    formatted_date = current_date.strftime("%Y-%m-%d")
    select_sql = "SELECT id,tag FROM tweet where end_dt = '9999-12-31' and start_dt < '{0}'".format(formatted_date)
    try:
        conn = sqlite3.connect('/Users/ddt/Documents/blockchain/smartwarm/swarms-twitter/test.db')
        c = conn.cursor()
        res = c.execute(select_sql)
        results = res.fetchall()
        conn.commit()
    except Exception as e:
        conn.close()
        raise
    finally:
        conn.close()
    return results


def update_openchain_tweet(tweet, tag):
    # 获取当前日期
    current_date = datetime.now()
    # 格式化日期为 yyyy - mm - dd 格式
    formatted_date = current_date.strftime("%Y-%m-%d")
    update_sql = "update tweet set end_dt='{0}' where id='{1}' and end_dt='9999-12-31'".format(formatted_date, tweet.id)
    try:
        conn = sqlite3.connect('/Users/ddt/Documents/blockchain/smartwarm/swarms-twitter/test.db')
        c = conn.cursor()
        c.execute(update_sql)
        conn.commit()

    except Exception as e:
        conn.close()
        raise
    finally:
        conn.close()
    add_tweet(tweet, tag)

def add_user_analysis(analysis:dict):
    insert_sql = "REPLACE INTO user_analysis (id,most_reply_tweet,most_like_tweet,most_view_tweet,most_retweet_tweet,most_engagements_tweet,total_likes,total_replies,total_views,total_retweets,engagement_rate,create_date) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}',{6},{7},{8},{9},{10},'{11}')".format(analysis["id"],analysis["most_reply_tweet"],analysis["most_like_tweet"],analysis["most_view_tweet"],analysis["most_retweet_tweet"],analysis["most_engagements_tweet"],analysis["total_likes"],analysis["total_replies"],analysis["total_views"],analysis["total_retweets"],analysis["engagement_rate"],analysis["create_date"])
    insert_sql_exec(insert_sql)