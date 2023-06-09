import os

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_TTL = int(os.environ['REDIS_TTL'])