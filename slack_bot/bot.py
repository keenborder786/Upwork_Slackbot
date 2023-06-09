import time

from selenium.common.exceptions import NoSuchElementException
from slack_bolt import App
from slack_bot.util import get_job_data , parse_generate_event_response
from slack.errors import SlackApiError
from upwork_bot import UpworkBot
from caching import Cache


## Global Parmeters which can be modified by user commands

KEEP_UPDATING = [True]

## Main function which starts our app and the revlevant responding functions
def start_app(slack_app_token, channel_id, redis_host, redis_ttl):
    """
    
    
    
    
    
    """
    app = App(token=slack_app_token)
    channel_id = channel_id
    cache_db = Cache(redis_host , redis_ttl)
    upwork_bot = UpworkBot(cache_db) # Starting the upwork_job
    
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
        """
        
        
        
        
        
        """
        ack("Hello. I am looking for the jobs. Please wait!")
        formatted_response = get_job_data(upwork_bot, body['text'])
        send_update(formatted_response)
    
    @app.shortcut("ge")
    def start_events(ack, body, logger,client):
        """
        
        
        
        """
        ack()
        res = client.views_open(
        trigger_id=body["trigger_id"],
        view= {
            "title": {
                "type": "plain_text",
                "text": "Job-Notifier"
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit"
            },
            "blocks": [
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "Job_Title",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "The Job Name for which you like to get the info"
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Job Name"
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "number_input",
                        "is_decimal_allowed": False,
                        "action_id": "Frequency"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "At what frequency(in minutes) which you like to get notify",
                        "emoji": True
                    }
                }
            ],
            "type": "modal"}
            )
    @app.view("")
    def handle_view_submission_events(ack, body, say, logger):
        """
        
        
        
        
        
        
        
        """
        ack()
        parameters = parse_generate_event_response(body)
        send_update(f"I will be updating you about the Job {parameters.get('Job_Title','')} after every {parameters.get('Frequency','')} minute(s)")

        KEEP_UPDATING[0] = True
        updates = 1
        while KEEP_UPDATING[0]:
            print(f"Number of updates posted {updates}")
            try:
                formatted_response = get_job_data(upwork_bot, parameters.get('Job_Title',''))
                send_update(formatted_response)
                time.sleep(int(parameters.get('Frequency',''))*60)
                updates+=1
            except Exception as e:
                print(f'An exception occured {e}')
                upwork_bot = UpworkBot(cache_db) # restarting the upwork bot
    @app.command('/stop')
    def stop_events(ack):
        """
        
        
        
        """
        ack()
        KEEP_UPDATING[0] = False
        send_update('The continuous notifier will be stopped.')



    return app
    


