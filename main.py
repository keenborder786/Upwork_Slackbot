
from slack_bot import Slackbot
from upwork_bot import UpworkBot
from caching import Cache
from slack_bolt.adapter.socket_mode import SocketModeHandler

from config import (
    SLACK_APP_TOKEN,CHANNEL_ID,
    SLACK_BOT_TOKEN,
    REDIS_HOST,
    REDIS_TTL)
import time

slack_bot = Slackbot(SLACK_BOT_TOKEN,CHANNEL_ID,REDIS_HOST,REDIS_TTL)
if __name__ == "__main__":
        handler = SocketModeHandler(slack_bot.app, SLACK_APP_TOKEN)
        handler.start()