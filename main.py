from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from twikit import Client
from TwitterOperationManager import TwitterOperationManager
import datetime
import time
from knowledge_base.meeting_notes import MeetingAssistant
from tools.document_reader import read_docx
import logging
from loguru import logger

def post_per_day(twitter_operation_manager:TwitterOperationManager):
    count=4
    global current_day, call_count
    today = datetime.date.today()
    if today != current_day:
        current_day = today
        call_count = 1
    if call_count > 4:
        return None
    twitter_operation_manager.post_per_day(call_count, count)
    call_count += 1


def main():
    load_dotenv()
    global current_day
    global call_count
    # logging.basicConfig(level=logging.INFO,filename="test.log",filemode='a',format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    # logging.info("This is a test logging message.")
    # # logger.add("loguru.log", format="{time} {level} {message}", level="INFO")
    # # logger.info("This is a test log message.")
    #
    # # 配置日志写入文件
    # logger.add("logfile.log", rotation="10 MB", compression="zip", encoding="utf-8",level="DEBUG")
    #
    # # 写不同级别的日志
    # logger.debug("This is a debug message")
    # logger.info("This is an info message")
    # logger.warning("This is a warning message")
    # logger.error("This is an error message")
    # logger.critical("This is a critical message")
    #
    # with open("logfile.log", "w") as f:
    #     f.write("Test log file permissions")

    current_day = datetime.date.today()
    call_count = 1
    product_whitepaper_path='/Users/ddt/Documents/blockchain/smartwarm/Contract Protocol White Paper-lite.docx'
    product_whitepaper=read_docx(product_whitepaper_path)
    account_handle='@Libert_ai'
    account_mission="""To promote the Contract Protocol as the world's first AI Agent DAC (Decentralized Autonomous Company) incubator platform. The focus is on highlighting its innovative approach to multi-agent collaboration, decentralized decision-making, and its role in building a vibrant ecosystem where AI agents and DACs work together to improve efficiency, adaptability, and sustainability. The mission includes driving engagement by showcasing its core offerings:
                        The talent marketplace for connecting DACs with AI agents for optimal task execution.
                        The commercial street for presenting DAC services and facilitating efficient business collaborations.
                        The ** $ CA token economy** to bolster platform sustainability and incentivize long-term participation.
                        Ultimately, the account aims to position Contract Protocol as a leading example of how multi-agent collaboration can redefine the future of intelligent business operations and decentralized organizations."""
    twitter_operation_manager = TwitterOperationManager(product_whitepaper=product_whitepaper,account_handle=account_handle,account_mission=account_mission)
    scheduler = BlockingScheduler()
    # 添加每日发推任务
    scheduler.add_job(post_per_day, 'cron', hour=1, minute=30,
                      kwargs={"twitter_operation_manager": twitter_operation_manager})
    scheduler.add_job(post_per_day, 'cron', hour=3, minute=30,
                      kwargs={"twitter_operation_manager": twitter_operation_manager})
    scheduler.add_job(post_per_day, 'cron', hour=5, minute=30,
                      kwargs={"twitter_operation_manager": twitter_operation_manager})
    scheduler.add_job(post_per_day, 'cron', hour=7, minute=30,
                      kwargs={"twitter_operation_manager": twitter_operation_manager})
    # 添加回复mention任务
    scheduler.add_job(twitter_operation_manager.reply_mentions,'interval',  hours=2)
    # 添加回复timeline任务
    scheduler.add_job(twitter_operation_manager.reply_timeline, 'interval', hours=2)
    # 添加查找价值用户任务
    scheduler.add_job(twitter_operation_manager.search_twitter_user, 'interval', hours=12)
    # 添加每日一会任务
    scheduler.add_job(twitter_operation_manager.daily_meeting, 'cron', hour=22,minute=0)
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()

    #twitter_operation_manager.reply_mentions()
    #twitter_operation_manager.reply_timeline()
    #twitter_operation_manager.search_twitter_user()
    #twitter_operation_manager.daily_meeting()
    # post_per_day(twitter_operation_manager)
    # time.sleep(60)
    # post_per_day(twitter_operation_manager)
    # time.sleep(60)
    # post_per_day(twitter_operation_manager)
    # time.sleep(60)
    # post_per_day(twitter_operation_manager)
    #
    # meetingAssistant = MeetingAssistant()
    # print(meetingAssistant.delete_meeting_notes_by_metadata({"date": '2025-02-26'}))




if __name__ == "__main__":
    main()