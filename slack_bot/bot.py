from slack_bolt import App
from slack.errors import SlackApiError
from slack_bolt.adapter.socket_mode import SocketModeHandler




class Slackbot:
    def __init__(self, slack_app_token,channel_id):
        """
        
        
        
        """
        self.app = App(token=slack_app_token)
        # ID of channel you want to post message to
        self.channel_id = channel_id
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
