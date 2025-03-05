from datetime import date, timedelta, datetime
import os
from swarms_fork.agent import Agent
from swarm_models import OpenAIChat
from swarms_fork.group_chat import AutoGroupMeeting
from knowledge_base.meeting_notes import MeetingAssistant
from tools.twitter_tookit import update_db_info, twitter_user_analysis, twitter_tweet_analysis
from tools.twitter_functions import TwitterFunction
from prompts.agent import (BRAND_TWITTER_AGENT_PROMPT, COMMUNITY_MANAGER_PROMPT, TWITTER_DATA_ANALYOR_PROMPT,ADMINISTRATIVE_ASSISTANT_PROMPT)
from prompts.task import *
import json
import ast

class TwitterAgent(Agent):
    def __init__(self, **kwargs, ):
        super().__init__(**kwargs)


class TwitterOperationManager:
    def __init__(self,
                 product_whitepaper: str = None,
                 account_handle: str = None,
                 account_mission: str = None
                 ):
        self.model = OpenAIChat(
            openai_api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-4o-mini", temperature=0.1,
            openai_api_base="https://api.mixrai.com/v1")
        self.product_whitepaper = product_whitepaper
        self.account_handle = account_handle
        self.account_mission = account_mission
        self._init_agent()

    def _init_agent(self):
        self.twitter_writer_cookies = {"auth_token": '6b352a60fc5b02c731f400b7c7a990759012810f',
                                       "ct0": 'c7689c3118648416c38e051b1ae7aed0311b92f3d935d1515d74eaab1767922057f1130cba27da60be5e99c24701d8b5f5739d8f65f97232476bf88414142598528fb2be7418bed212e0c97a9325567f'}
        self.twitter_writer_function = TwitterFunction(cookies=self.twitter_writer_cookies,
                                                       account_handle=self.account_handle)
        self.twitter_writer = Agent(
            agent_name="BRAND_TWITTER_AGENT",
            agent_description=BRAND_TWITTER_AGENT_PROMPT,
            llm=self.model,
            autosave=True,
            dashboard=False,
            verbose=True,
            max_loops=1,
            tool_system_prompt=None,
            metadata_output_type="json",
            function_calling_format_type="OpenAI",
            function_calling_type="json",  # or soon yaml
            product_whitepaper=self.product_whitepaper,
            account_handle=self.account_handle,
            account_mission=self.account_mission,
        )
        self.twitter_data_analyst_cookies = {"auth_token": '6b352a60fc5b02c731f400b7c7a990759012810f',
                                             "ct0": 'c7689c3118648416c38e051b1ae7aed0311b92f3d935d1515d74eaab1767922057f1130cba27da60be5e99c24701d8b5f5739d8f65f97232476bf88414142598528fb2be7418bed212e0c97a9325567f'}
        self.twitter_data_analyst_function = TwitterFunction(cookies=self.twitter_data_analyst_cookies,
                                                             account_handle=self.account_handle)
        self.twitter_data_analyst = Agent(
            agent_name="TWITTER_DATA_ANALYOR",
            agent_description=TWITTER_DATA_ANALYOR_PROMPT,
            llm=self.model,
            autosave=True,
            dashboard=False,
            verbose=True,
            max_loops=1,
            tool_system_prompt=None,
            metadata_output_type="json",
            function_calling_format_type="OpenAI",
            function_calling_type="json",  # or soon yaml
            product_whitepaper=self.product_whitepaper,
            account_handle=self.account_handle,
            account_mission=self.account_mission,
        )
        self.twitter_publicist_cookies = {"auth_token": '6b352a60fc5b02c731f400b7c7a990759012810f',
                                          "ct0": 'c7689c3118648416c38e051b1ae7aed0311b92f3d935d1515d74eaab1767922057f1130cba27da60be5e99c24701d8b5f5739d8f65f97232476bf88414142598528fb2be7418bed212e0c97a9325567f'}
        self.twitter_publicist_function = TwitterFunction(cookies=self.twitter_publicist_cookies,
                                                          account_handle=self.account_handle)
        self.twitter_publicist = Agent(
            agent_name="COMMUNITY_MANAGER",
            agent_description=COMMUNITY_MANAGER_PROMPT,
            llm=self.model,
            autosave=True,
            dashboard=False,
            verbose=True,
            max_loops=1,
            tool_system_prompt=None,
            metadata_output_type="json",
            function_calling_format_type="OpenAI",
            function_calling_type="json",  # or soon yaml
            product_whitepaper=self.product_whitepaper,
            account_handle=self.account_handle,
            account_mission=self.account_mission,
        )
        self.administrative_assistant = Agent(
            agent_name="ADMINISTRATIVE_ASSISTANT",
            system_prompt=ADMINISTRATIVE_ASSISTANT_PROMPT,
            agent_description=None,
            llm=self.model,
            autosave=True,
            dashboard=False,
            verbose=True,
            max_loops=1,
            tool_system_prompt=None,
            metadata_output_type="json",
            function_calling_format_type="OpenAI",
            function_calling_type="json",  # or soon yaml
            product_whitepaper=self.product_whitepaper,
            account_handle=self.account_handle,
            account_mission=self.account_mission,
        )


    def post_per_day(self, trun, count):
        # 获取当前日期
        today = date.today()
        # 计算昨日日期，通过当前日期减去一天的时间间隔
        yesterday = today - timedelta(days=1)
        meetingAssistant = MeetingAssistant()
        notes = meetingAssistant.query_meeting_notes_by_metadata( {"$and": [{'date': str(yesterday)},{'topic': 'daily meeting'}]})
        if len(notes) >0 :
            note = ast.literal_eval(notes[0][0].page_content)[-1]
        else:
            note = ''
        prompt = daily_post_prompt(note, trun, count)
        print(prompt)
        twitter_poster = Agent(
            agent_name="BRAND_TWITTER_AGENT",
            agent_description=BRAND_TWITTER_AGENT_PROMPT,
            llm=self.model,
            preset_stopping_token=True,
            dynamic_loops=True,
            autosave=True,
            dashboard=False,
            verbose=True,
            tools=[self.twitter_writer_function.post_tweet, self.twitter_writer_function.reply_tweet,
                   self.twitter_writer_function.like_tweet, self.twitter_writer_function.retweet,
                   self.twitter_writer_function.get_tweet_timeline, self.twitter_writer_function.search_tweet,
                   self.twitter_writer_function.follow_user, self.twitter_writer_function.get_mentions],
            # long_term_memory=chromadb,
            metadata_output_type="json",
            # List of schemas that the agent can handle
            # list_base_models=[tool_schema],
            function_calling_format_type="OpenAI",
            function_calling_type="json",  # or soon yaml
            product_whitepaper=self.product_whitepaper,
            account_handle=self.account_handle,
            account_mission=self.account_mission,
        )
        twitter_poster.run(prompt)

    def reply_mentions(self):
        prompt = reply_prompt
        twitter_replyer = Agent(
            agent_name="BRAND_TWITTER_AGENT",
            agent_description=BRAND_TWITTER_AGENT_PROMPT,
            llm=self.model,
            preset_stopping_token=True,
            dynamic_loops=True,
            autosave=True,
            dashboard=False,
            verbose=True,
            saved_state_path="finance_agent.json",
            tools=[self.twitter_writer_function.post_tweet, self.twitter_writer_function.reply_tweet,
                   self.twitter_writer_function.like_tweet, self.twitter_writer_function.retweet,
                   self.twitter_writer_function.get_tweet_timeline, self.twitter_writer_function.search_tweet,
                   self.twitter_writer_function.follow_user, self.twitter_writer_function.get_mentions],
            # long_term_memory=chromadb,
            metadata_output_type="json",
            # List of schemas that the agent can handle
            # list_base_models=[tool_schema],
            function_calling_format_type="OpenAI",
            function_calling_type="json",  # or soon yaml
            product_whitepaper=self.product_whitepaper,
            account_handle=self.account_handle,
            account_mission=self.account_mission,
        )
        twitter_replyer.run(prompt)

    def search_twitter_user(self):
        prompt = search_twitter_prompt_v2
        twitter_searcher = Agent(
            agent_name="COMMUNITY_MANAGER",
            agent_description=COMMUNITY_MANAGER_PROMPT,
            llm=self.model,
            preset_stopping_token=True,
            dynamic_loops=True,
            max_loops=10,
            autosave=True,
            dashboard=False,
            verbose=True,
            saved_state_path="finance_agent.json",
            tools=[self.twitter_publicist_function.post_tweet, self.twitter_publicist_function.reply_tweet,
                   self.twitter_publicist_function.like_tweet, self.twitter_publicist_function.retweet,
                   self.twitter_publicist_function.get_tweet_timeline, self.twitter_publicist_function.search_tweet,
                   self.twitter_publicist_function.follow_user, self.twitter_publicist_function.get_mentions,
                   self.twitter_writer_function.search_user_tweet],
            # long_term_memory=chromadb,
            metadata_output_type="json",
            # List of schemas that the agent can handle
            # list_base_models=[tool_schema],
            function_calling_format_type="OpenAI",
            function_calling_type="json",  # or soon yaml
            product_whitepaper=self.product_whitepaper,
            account_handle=self.account_handle,
            account_mission=self.account_mission,
        )
        twitter_searcher.run(prompt)

    def reply_timeline(self):
        timeline_tweets = self.twitter_publicist_function.get_tweet_timeline()
        prompt = reply_timeline(timeline_tweets)
        twitter_replyer = Agent(
            agent_name="BRAND_TWITTER_AGENT",
            agent_description=BRAND_TWITTER_AGENT_PROMPT,
            llm=self.model,
            preset_stopping_token=True,
            dynamic_loops=True,
            autosave=True,
            dashboard=False,
            verbose=True,
            saved_state_path="finance_agent.json",
            tools=[self.twitter_writer_function.post_tweet, self.twitter_writer_function.reply_tweet,
                   self.twitter_writer_function.like_tweet, self.twitter_writer_function.retweet,
                   self.twitter_writer_function.get_tweet_timeline, self.twitter_writer_function.search_tweet,
                   self.twitter_writer_function.follow_user, self.twitter_writer_function.get_mentions],
            # long_term_memory=chromadb,
            metadata_output_type="json",
            # List of schemas that the agent can handle
            # list_base_models=[tool_schema],
            function_calling_format_type="OpenAI",
            function_calling_type="json",  # or soon yaml
            product_whitepaper=self.product_whitepaper,
            account_handle=self.account_handle,
            account_mission=self.account_mission,
        )
        twitter_replyer.run(prompt)

    def daily_meeting(self):
        ##更新数据库
        update_db_info()
        ##查询数据库，得到统计分析数据
        owner_account_data = twitter_user_analysis('owner', 7)
        competitor_account_data = twitter_user_analysis('competitor', 7)
        owner_tweets_data = twitter_tweet_analysis('owner', 7)
        competitor_tweets_data = twitter_tweet_analysis('competitor', 7)
        prompt = daily_regular_meeting_prompt(owner_account_data, competitor_account_data, owner_tweets_data,
                                              competitor_tweets_data)
        ##发起会议，并保存会议结果
        agents = [self.twitter_data_analyst, self.twitter_publicist, self.twitter_writer]
        chat = AutoGroupMeeting(
            name="Daily meeting",
            description="Discussion on Twitter Operation Strategy",
            agents=agents,
            assistant_agent=self.administrative_assistant,
        )
        chat.auto_run(
            prompt
        )
        meeting_note = chat.get_full_chat_history()
        current_date = datetime.now()
        # 格式化日期为 yyyy - mm - dd 格式
        formatted_date = current_date.strftime("%Y-%m-%d")
        note = {'date': formatted_date, 'topic': "daily meeting", 'content': str(meeting_note)}
        meetingAssistant = MeetingAssistant()
        meetingAssistant.save_meeting_notes([note])

        #print(meetingAssistant.delete_meeting_notes_by_metadata({"date": '2025-02-25'}))
