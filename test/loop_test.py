import os
from swarms import Agent
from swarm_models import OpenAIChat
from dotenv import load_dotenv
import asyncio

from twikit import Client,Tweet
from httpx import Response
import json
import platform
import trio

load_dotenv()
cookies = {"auth_token": '6b352a60fc5b02c731f400b7c7a990759012810f',
           "ct0": 'c7689c3118648416c38e051b1ae7aed0311b92f3d935d1515d74eaab1767922057f1130cba27da60be5e99c24701d8b5f5739d8f65f97232476bf88414142598528fb2be7418bed212e0c97a9325567f'}
client = Client('en-US')
client.set_cookies(cookies)

def post_tweet(content: str,media_ids:list[str]| None = None):
    """
    Post an original tweet. Use this to share new ideas, thoughts, or start conversations without referencing a tweet. You may choose to attach medias with the post. Avoid mentioning polls or spaces. You don’t have to plan any related follow-up action/ search for replies as this will be handled in your reaction module.

    Args:
        content (str): The content of the tweet. Make sure it is concise. Do not include hashtag. Keep it within 70 words.
        media_ids (list[str]| None):  A list of media IDs or URIs to attach to the tweet.media IDs can be obtained by using the `upload_media` method. Optional, only if you want to attach medias.

    Returns:
        Twitter: The Created Tweet.
    """

    new_loop = asyncio.get_event_loop()
    asyncio.set_event_loop(new_loop)
    try:
        tweet = new_loop.run_until_complete(client.create_tweet(content,media_ids))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        new_loop.close()
    return tweet

def like_tweet(tweet_id:str):
    """
    Like a tweet. Choose this when you want to support a tweet quickly, without needing to comment.
    Args:
        tweet_id (str): Tweet ID to like.
    Returns:
        httpx.Response: Response returned from twitter api.
    """

    new_loop = asyncio.new_event_loop()
    print("newloop status " + str(new_loop.is_closed()))
    #asyncio.set_event_loop(new_loop)
    try:
        tweet = new_loop.run_until_complete(client.get_tweet_by_id(tweet_id))
    except Exception as e:
        print(f"An error occurred get tweet: {e}")
    # finally:
    #     new_loop.close()

    new_loop = asyncio.get_event_loop()
    asyncio.set_event_loop(new_loop)
    try:
        response = new_loop.run_until_complete(tweet.favorite())
    except Exception as e:
        print(f"An error occurred when favorite: {e}")
    # finally:
    #     new_loop.close()

    # response = asyncio.run(_like_tweet(tweet_id))
    if response.status_code ==200:
        return 'Successfully liked the tweet with the ID of {}.'.format(tweet_id)
    else:
        return 'Failed liked the tweet,because: {}'.format(json.load(response.text)["message"])

#
#
#
# print(platform.system())
# if platform.system() == 'Windows':
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# out=post_tweet("te23sdfsdfaadsd1")
# print(out)


# new_loop = asyncio.new_event_loop()
# tweet = new_loop.run_until_complete(client.get_tweet_by_id("1882473564932301144"))
# # out=asyncio.run(client.get_tweet_by_id("1882473564932301144"))
# print(tweet)

out=trio.run(lambda: client.get_tweet_by_id("1882473564932301144"))
out=trio.run(lambda: client.get_tweet_by_id("1882473564932301144"))

# out=like_tweet("1882473564932301144")
print(out)



# async def test():
#     print("test")
#     return "success"
#
# async def main():
#     a= await test()
#     print(a)
#
#
# asyncio.run(main())


#asyncio.run(create_twitter("hello agent"))


    # Initialize the agent

    # Run the agent on a financial query
    #out = agent_twitter.run("你是一个twitter运营员，你可以使用工具获取到twitter最近的消息，请首先使用get_tweet_timeline获取新的tweets（可能会获取到多条），然后阅读获取到的每条tweet，接着对你感兴趣的tweet做你想做的操作，例如发推、转推、点赞、评论等等")
    #out = agent_twitter.run("你是一个twitter运营员，你可以使用工具获取到twitter最近的消息，请首先使用get_tweet_timeline获取新的tweets（只获取一条），然后对这条tweet点赞")
    # out = agent.run("请分别给出北京、上海和天津三地的玫瑰花的平均价格")

    # out= like_tweet('1882473564932301144')
    # post_tweet = post_tweet('test ai !')
    # print(out)
    # print(post_tweet)
    #print(get_mentions())
    #update_db_info()