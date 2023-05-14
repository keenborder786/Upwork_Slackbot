import upwork
from pprint import pprint
from upwork.routers import auth

class Client:
    
    def __init__(self, consumer_key,consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

def start_desktop_client(self):
    """


    """
    config = upwork.Config(
        {
            "client_id": self.consumer_key,
            "client_secret": self.consumer_secret,
            "redirect_uri": "https://a.callback.url",
        }
    )
    self.client = upwork.Client(config) ## Authorization
    try:
        config.token
    except AttributeError: ## Setting up token for upwork client
        authorization_url, state = self.client.get_authorization_url()
        authz_code = input(
            "Please enter the full callback URL you get "
            "following this link:\n{0}\n\n> ".format(authorization_url)
        ) ## TODO: Get Auth Code Directly from https://www.upwork.com/ab/account-security/oauth2/authorize?response_type=token&client_id=CLIENT-ID-HERE&redirect_uri=https://a.callback.url
        self.client.get_access_token(authz_code)
