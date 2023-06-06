from selenium.common.exceptions import NoSuchElementException
from slack_bolt import App
from slack.errors import SlackApiError
from upwork_bot import UpworkBot
from caching import Cache
import time
class Slackbot:
    def __init__(self, slack_app_token,channel_id ,redis_host , redis_ttl):
        """
        
        
        
        """
        self.app = App(token=slack_app_token)
        # ID of channel you want to post message to
        self.channel_id = channel_id
        self.cache_db = Cache(redis_host , redis_ttl)
        self.upwork_bot = UpworkBot(self.cache_db)
        self.start_events()
    def send_update(self,message_payload):
        """
        
        
        
        """
        try:
            # Call the conversations.list method using the WebClient
            result = self.app.client.chat_postMessage(
                channel=self.channel_id,
                text = message_payload,
                mrkdwn=True
            )
        except SlackApiError as e:
            print(f"Error: {e}")
    
    
    def start_events(self):
        @self.app.command("/generate")
        def func(ack , body):
            ack("Hello. I am looking for the jobs. Please wait!")
            ## Now make it loop with specific time interval (How do I extract the specific parameters from user response???)
            html_data = self.upwork_bot.get_data(body['text'])
            jobs_data = self.upwork_bot.parse_data(html_data)
            formatted_response = self.upwork_bot.format_data(jobs_data)
            self.send_update(formatted_response)
        return func
