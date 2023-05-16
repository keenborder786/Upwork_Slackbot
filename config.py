import os
from dotenv import load_dotenv

load_dotenv()
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
QUERY = os.environ['QUERY']
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']