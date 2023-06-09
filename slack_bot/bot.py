import time

import slack_bolt
import slack_sdk

from typing import Dict,Any

from selenium.common.exceptions import NoSuchElementException
from slack_bolt import App
from slack_bot.util import get_job_data , parse_generate_event_response
from slack.errors import SlackApiError
from upwork_bot import UpworkBot
from caching import Cache


## Global Parmeters which can be modified by user commands

KEEP_UPDATING = [True]

def start_app(slack_app_token:str, channel_id:str, redis_host:str, redis_ttl:int) -> "slack_bolt.App":
    """Main function which starts the Slack Bolt App and registers the functions needed
    for the app to function.

    Parameters
    ----------

    slack_app_token : str 
        The App token generated.
    channel_id : str
        The channel id on the slack where the bot is supposed to send the events
    redis_host : str
        The endpoint for redis cluster
    redis_ttl : str
        Time to live for redis key/value pair

    Returns
    -------
    slack_bolt.App
        Slack Bolt App Client.
    
    """
    app = App(token=slack_app_token)
    channel_id = channel_id
    cache_db = Cache(redis_host , redis_ttl)
    upwork_bot = UpworkBot(cache_db) # Starting the upwork_job
    
    def send_update(message_payload:str) -> None:
        """Send the message to your user

        Parameters
        ----------

        message_payload : str
            Message text to send to the user
        
        Returns
        -------
        None
        
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
    def generate_event(ack:slack_bolt.Ack, body:Dict[str, Any]) -> None:
        """Gives Job Posting to the user when they type `/generate` command

        Parameters:
        ----------

        ack : slack_bolt.Ack
            `ack()` utility function, which returns acknowledgement to the Slack servers
        body : Dict[str,Any]
            Parsed request body data coming from slack server
        
        Returns
        -------
        None

        """
        ack("Hello. I am looking for the jobs. Please wait!")
        formatted_response = get_job_data(upwork_bot, body['text'])
        send_update(formatted_response)
    
    @app.shortcut("ge")
    def start_events(ack:slack_bolt.Ack, body:Dict[str, Any], client:slack_sdk.WebClient) -> None:
        """Pops the Input Modal on slack when user starts the `Generate-Events` event

        Parameters:
        ----------

        ack : slack_bolt.Ack
            `ack()` utility function, which returns acknowledgement to the Slack servers
        body : Dict[str,Any]
            Parsed request body data coming from slack server
        client : slack_sdk.WebClient
            `slack_sdk.web.WebClient` instance with a valid token
        
        Returns
        -------
        None
        
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
    def handle_view_submission_events(ack:slack_bolt.Ack, body:Dict[str, Any]) -> None:
        """Start generating Job Notifications for the user given the input from the `Generate-Events` modal

        Parameters:
        ----------

        ack : slack_bolt.Ack
            `ack()` utility function, which returns acknowledgement to the Slack servers
        body : Dict[str,Any]
            Parsed request body data coming from slack server
        client : slack_sdk.WebClient
            `slack_sdk.web.WebClient` instance with a valid token
        
        Returns
        -------
        None
        
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
    def stop_events(ack:slack_bolt.Ack) -> None:
        """Stop the `Generate-Events` event and inform user

        Parameters:
        ----------

        ack : slack_bolt.Ack
            `ack()` utility function, which returns acknowledgement to the Slack servers        
                
        Returns
        -------
        None
        
        """
        ack()
        KEEP_UPDATING[0] = False
        send_update('The continuous notifier will be stopped.')



    return app
    


