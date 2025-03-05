from twikit import Client, Tweet
import trio

from tools.twitter_tookit import addTweetInfoToDB, addUserInfoToDB
import json


class TwitterFunction():
    def __init__(self, cookies, account_handle):
        self.cookies = cookies
        self.client = Client('en-US')
        self.client.set_cookies(self.cookies)
        self.account_handle = account_handle

    def post_tweet(self, content: str, media_ids: list[str] | None = None, addWatchList: bool = True):
        """
        Post an original tweet. Use this to share new ideas, thoughts, or start conversations without referencing a tweet. You may choose to attach medias with the post. Avoid mentioning polls or spaces. You don’t have to plan any related follow-up action/ search for replies as this will be handled in your reaction module.

        Args:
            content (str): The content of the tweet. Make sure it is concise. Do not include hashtag. Keep it within 70 words.
            media_ids (list[str]| None):  A list of media IDs or URIs to attach to the tweet.media IDs can be obtained by using the `upload_media` method. Optional, only if you want to attach medias.

        Returns:
            str: Inform whether the tweet was posted successfully.
        """
        try:
            tweet = trio.run(lambda: self.client.create_tweet(content, media_ids))
            if addWatchList:
                addTweetInfoToDB(tweet)
        except Exception as e:
            print('Failed to post the tweet,because: {0}. Please try again.'.format(str(e)))
            raise
        return 'Successfully posted the tweet.'

        return tweet

    def reply_tweet(self, tweet_id: str, content: str, media_ids: list[str] | None = None):
        """
        Respond directly to another tweet. Use this when you want to engage in a conversation, ask a question, or provide feedback directly to the tweet author or thread. You may choose to attach medias with the post. Avoid mentioning polls or spaces.
        Args:
            tweet_id (str): Tweet ID to reply to.
            content (str): The text content of the reply. Make sure it is concise. Do not include hashtag. Keep it within 70 words.
            media_ids (list[str]| None):  A list of media IDs or URIs to attach to the tweet.media IDs can be obtained by using the `upload_media` method. Optional, only if you want to attach medias.
        Returns:
            str: Inform whether the tweet reply was successful.
        """
        try:
            tweet = trio.run(lambda: self.client.get_tweet_by_id(tweet_id))
            return_tweet = trio.run(lambda: tweet.reply(content, media_ids))
        except Exception as e:
            return 'Failed to reply to the tweet with ID {},because: {}. Please try again.'.format(tweet_id, str(
                e))
        return 'Successfully replied to the tweet with ID  {}.'.format(tweet_id)

    def like_tweet(self, tweet_id: str):
        """
        Like a tweet. Choose this when you want to support a tweet quickly, without needing to comment.
        Args:
            tweet_id (str): Tweet ID to like.
        Returns:
            str: Inform whether the tweet was liked successfully.
        """
        try:
            tweet = trio.run(lambda: self.client.get_tweet_by_id(tweet_id))
            response = trio.run(lambda: tweet.favorite())

            # response = asyncio.run(_like_tweet(tweet_id))
            if response.status_code == 200:
                return 'Successfully liked the tweet with ID  {}.'.format(tweet_id)
            else:
                return 'Failed to like the tweet with ID {},because: {}. Please try again.'.format(tweet_id, str(
                    json.load(response.text)["message"]))
        except Exception as e:
            return 'Failed to like the tweet with ID {},because: {}. Please try again.'.format(tweet_id, str(
                json.load(response.text)["message"]))

    def retweet(self, tweet_id: str, content: str):
        """
            Share a tweet as-is, without adding your own input. Choose this when you want to amplify or support a tweet quickly, without needing to add any commentary or opinion. This will help with your social presence.
            Args:
                tweet_id (str): Tweet ID to quote.
            Returns:
                str: Inform whether the retweet was successful.
        """
        try:
            tweet = trio.run(lambda: self.client.get_tweet_by_id(tweet_id))
            response = trio.run(lambda: tweet.retweet())
            if response.status_code == 200:
                return 'Successfully retweeted the tweet with ID {}.'.format(tweet_id)
            else:
                return 'Failed to retweet the tweet with ID {},because: {}. Please try again.'.format(tweet_id, str(
                    json.load(response.text)["message"]))
        except Exception as e:
            return 'Failed to retweet the tweet with ID {},because: {}. Please try again.'.format(tweet_id, str(
                e))

    def search_internet(question: str):
        """
            Search internet for latest information and knowledge. Do no use this to search for token related information and tweet related.
            Args:
                question (str): The question you wish to ask.
            Returns:
                str : answer from internet
        """

    def get_tweet_timeline(self, count: int = 20, ):
        """
                Retrieves tweets from Home -> For You.
                Args:
                    count (int): The number of tweets to retrieve.
                Returns:
                    list[dict] | str : A Result list containing a list of Tweet objects or error descriptions.
            """
        try:
            result = trio.run(lambda: self.client.get_timeline(count))
            tweet_result = []
            for tweet in result[:count]:
                subTweet = {"tweet_id": tweet.id, "user": tweet.user.id, "create_time": tweet.created_at_datetime,
                            "favorite count": tweet.favorite_count, "retweet count": tweet.retweet_count,
                            "quote count": tweet.quote_count, "reply count": tweet.reply_count,
                            "view count": tweet.view_count, "content": tweet.text}  # ,"media":tweet.media}
                tweet_result.append(subTweet)
        except Exception as e:
            return f"Error occurred while fetching the tweet timeline. Please try again."
        return tweet_result

    def search_tweet(self, query: str, count: int = 20):
        """
                    Search for the latest tweets on Twitter based on the given keywords.
                    Args:
                        query (str): The search query.
                        count (int): The number of tweets to retrieve.
                    Returns:
                        list[dict] | strstr : A Result list containing the search results and user info. or error descriptions.
                """
        try:
            result = trio.run(lambda: self.client.search_tweet(query, count=count,product='Latest'))
            tweet_result = []
            for tweet in result[:count]:
                subTweet = {"tweet id": tweet.id, "user id": tweet.user.id, "create_time": tweet.created_at_datetime,
                            "favorite count": tweet.favorite_count, "retweet count": tweet.retweet_count,
                            "quote count": tweet.quote_count, "reply count": tweet.reply_count,
                            "view count": tweet.view_count, "content": tweet.text,"user name":tweet.user.screen_name,
                            "user description": tweet.user.description,
                            "user followers count": tweet.user.followers_count}  # ,"media":tweet.media}
                tweet_result.append(subTweet)
        except Exception as e:
            return "Error occurred while searching tweet about {0} .Because {1}. Please try again.".format(query,
                                                                                                            str(e))
        return tweet_result

    def search_user_tweet(self, userList: list, tweetCount: int = 10):
        """
                Search for tweets from a specified Twitter user list
                Args:
                    userList (list): A list of user IDs for which tweets need to be searched.
                    count (int): The number of tweets to retrieve.
                Returns:
                    list[dict] | str : A Result list containing each user‘s search results and user id or error descriptions.The structure of the dictionary is as follows:
                                  - 'user_id' (str): The user's id.
                                  - 'user_tweet' (list): A Result list containing the search tweets abort this user.
            """
        res = []
        try:
            for userId in userList:
                user_tweet = {}
                user = trio.run(lambda: self.client.get_user_by_id(userId))
                result = trio.run(lambda: user.get_tweets('Tweets', tweetCount))
                tweet_result = []
                for tweet in result[:tweetCount]:
                    subTweet = {"tweet id": tweet.id,"create time": tweet.created_at_datetime,
                                "favorite count": tweet.favorite_count, "retweet count": tweet.retweet_count,
                                "quote count": tweet.quote_count, "reply count": tweet.reply_count,
                                "view count": tweet.view_count,
                                "content": tweet.text}  # ,"media":tweet.media}
                    tweet_result.append(subTweet)
                user_tweet["user_id"] = user.id
                user_tweet["user_tweet"] = tweet_result
                res.append(user_tweet)
        except Exception as e:
            return "Error occurred while searching user tweet.Because {0}. Please try again.".format(str(e))
        return res

    def follow_user(self, userList: list, addWatchlist: bool):
        """
            follow the given users
            Args:
                userList (list): A list of user IDs needed to be followed.
                addWatchlist (bool): Whether the user needs to be added to the watchlist (generally applicable when looking for competitor users,KOL is not needed.).
            Returns:
                str : Inform whether the all the follow actions were successful.
                """
        try:
            for userId in userList:
                user = trio.run(lambda: self.client.get_user_by_id(userId))
                trio.run(lambda: user.follow())
                if addWatchlist:
                    addUserInfoToDB(user.id)
        except Exception as e:
            return "Error occurred while following user.Because {0}. Please try again.".format(str(e))
        return "Successfully followed the given users"

    def get_mentions(self):
        """
           Retrieve mention messages from Twitter account notifications, including tweets where other accounts @mention you or reply to your tweets that you have not yet responded to.
           Returns:
               list[dict] | str : A Result list containing the search results or error descriptions.
           """
        username = self.account_handle
        reply_tweets = []
        tweets = trio.run(lambda: self.client.search_tweet(username, 'Latest'))
        for tweet in tweets:
            if username + ' ' in tweet.full_text:
                tweet = trio.run(lambda: self.client.get_tweet_by_id(tweet.id))
                isReply = False;
                if len(tweet.replies) > 0:
                    for replyTweet in tweet.replies:
                        if replyTweet.user.screen_name == username[1:]:
                            isReply = True
                            break;
                if not isReply:
                    subTweet = {"tweet_id": tweet.id, "user": tweet.user.id, "create_time": tweet.created_at_datetime,
                                "favorite count": tweet.favorite_count, "retweet count": tweet.retweet_count,
                                "quote count": tweet.quote_count, "reply count": tweet.reply_count,
                                "view count": tweet.view_count,
                                "content": tweet.full_text}
                    reply_tweets.append(subTweet)
        return reply_tweets

if __name__ == "__main__":
    twitter_writer_cookies = {"auth_token": '6b352a60fc5b02c731f400b7c7a990759012810f',
                                   "ct0": 'c7689c3118648416c38e051b1ae7aed0311b92f3d935d1515d74eaab1767922057f1130cba27da60be5e99c24701d8b5f5739d8f65f97232476bf88414142598528fb2be7418bed212e0c97a9325567f'}
    account_handle = '@Libert_ai'
    twitter_writer_function = TwitterFunction(cookies=twitter_writer_cookies,
                                                   account_handle=account_handle)
    res=twitter_writer_function.search_tweet("AI trends OR blockchain collaboration OR future of work")
    print(res)