import requests
import os
import pandas as pd
import json
import random


class Scrapper:

    def __init__(self):

        self.url = "https://www.upwork.com/nx/jobs/search/?q=Ruby%20on%20Rails&sort=recency"
        self.df_user_agent_list = self._get_user_agent_df()['USER_AGENT'].values.tolist()
        self.proxies = self._get_proxies()

    def _get_user_agent_df(self):
        """
        Gets the User Agent DataFrame consisting of User Agent headers

        """
        dataframes = os.listdir('scrapper/data/user-agents')
        main_df = pd.DataFrame()
        for df in dataframes:
            if main_df.empty:
                main_df = pd.read_csv(f'scrapper/data/user-agents/{df}', encoding="ISO-8859-1")
            else:
                main_df = pd.concat([main_df, pd.read_csv(
                    f'scrapper/data/user-agents/{df}', encoding="ISO-8859-1")], axis=0)
        return main_df

    def _get_proxies(self):
        """
        Get Proxy List from the proxylist.geonode.com API.

        """
        return json.loads(requests.get(
            'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc').text)['data']

    def get_random_user_agent(self):
        """

        Takes a random user agent header

        """

        return self.df_user_agent_list[random.randint(0, len(self.df_user_agent_list) - 1)]

    def get_random_proxy(self):
        """
        Takes a random proxy

        """

        return self.proxies[random.randint(0, len(self.proxies) - 1)]


scrapper = Scrapper()
print(scrapper.get_random_user_agent())
print(scrapper.get_random_proxy())
