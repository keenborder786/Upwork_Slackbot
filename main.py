from slack_bot import Slackbot
from upwork_bot import UpworkBot
import time
from config import (
    QUERY,
    SLACK_APP_TOKEN,CHANNEL_ID)
slack_bot = Slackbot(SLACK_APP_TOKEN,CHANNEL_ID)
upwork_bot = UpworkBot(QUERY)
i = 1
## TO-DO: 
    ## Duration , Experience Level, Project Type
    ## Caching ---> Removing (After 12 Hours Removal)- Wipe out Option
    ## DB storage ---> Redis (Caching)
while True:
    print(f'Stress Testing Run: {i}')
    html_data = upwork_bot.get_data()
    jobs_data = upwork_bot.parse_data(html_data)
    formatted_response = upwork_bot.format_data(jobs_data)
    slack_bot.send_update(formatted_response)
    time.sleep(1.5)
    i+=1