from selenium.common.exceptions import NoSuchElementException
from slack_bolt import App
from slack.errors import SlackApiError
from upwork_bot import UpworkBot
from caching import Cache
import time



## Main function which starts our app and the revlevant responding functions
def start_app(slack_app_token,channel_id ,redis_host , redis_ttl):
    """
    
    
    
    
    
    """
    app = App(token=slack_app_token)
    channel_id = channel_id
    cache_db = Cache(redis_host , redis_ttl)
    upwork_bot = UpworkBot(cache_db)
    
    def send_update(message_payload):
        """
        
        
        
        """
        try:
            # Call the conversations.list method using the WebClient
            result = app.client.chat_postMessage(
                channel=channel_id,
                text = message_payload,
                mrkdwn=True
            )
        except SlackApiError as e:
            print(f"Error: {e}")
    
    @app.command("/generate")
    def generate_event(ack , body):
        ack("Hello. I am looking for the jobs. Please wait!")
        html_data = upwork_bot.get_data(body['text'])
        jobs_data = upwork_bot.parse_data(html_data)
        formatted_response = upwork_bot.format_data(jobs_data)
        send_update(formatted_response)
    
    @app.shortcut("ge")
    def start_events(ack, body, logger,client):
        ack()
        print(body)

        res = client.views_open(
            trigger_id=body["trigger_id"],
        view={
    "type": "modal",
    "callback_id": "modal-identifier",
    "title": {
        "type": "plain_text",
        "text": "Just a modal"
    },
    "blocks": [
        {
        "type": "section",
        "block_id": "section-identifier",
        "text": {
            "type": "mrkdwn",
            "text": "*Welcome* to ~my~ Block Kit _modal_!"
        },
        "accessory": {
            "type": "button",
            "text": {
            "type": "plain_text",
            "text": "Just a button",
            },
            "action_id": "button-identifier",
        }
        }
    ],
    }
        )
    

    return app
    


