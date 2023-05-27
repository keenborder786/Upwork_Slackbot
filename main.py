from selenium.common.exceptions import NoSuchElementException
from slack_bot import Slackbot
from upwork_bot import UpworkBot
from caching import Cache

from config import (
    QUERY,
    SLACK_APP_TOKEN,CHANNEL_ID,
    REDIS_HOST,
    REDIS_TTL)
import time

slack_bot = Slackbot(SLACK_APP_TOKEN,CHANNEL_ID)
cache_db = Cache(REDIS_HOST , REDIS_TTL)
upwork_bot = UpworkBot(QUERY , cache_db)

i = 1
while True:
    try:
        print(f'Running the Bot. Number of updates send: {i}')
        html_data = upwork_bot.get_data()
        jobs_data = upwork_bot.parse_data(html_data)
        formatted_response = upwork_bot.format_data(jobs_data)
        slack_bot.send_update(formatted_response)
        i+=1
        time.sleep(0.25)
    except NoSuchElementException:
        print('No Element Exception raised by selenium. Resetting the bot')
        upwork_bot.driver.quit()
        upwork_bot = UpworkBot(QUERY) ## Recreating the bot.
        time.sleep(5)

    