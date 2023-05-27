from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_headers import Headers
import json
class UpworkBot:
    def __init__(self,query, cache_db):
        """
        
        
        """
        self.query = query
        self.cache_db = cache_db
        self.driver = self._intialize_driver()
    def _intialize_driver(self):

        """
        
        
        
        """
        options = Options()
        header = Headers(
            browser="chrome",  # Generate only Chrome UA
            os="win",  # Generate only Windows platform
            headers=False # generate misc headers
        )
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        customUserAgent = header.generate()['User-Agent']
        options.add_argument(f"user-agent={customUserAgent}") # head a fake-header to work in headless mode.
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(f"https://www.upwork.com/nx/jobs/search/?q={self.query.replace(' ','%20')}&sort=recency")
        return driver

    def get_data(self):

        """
        
        
        """
        
        jobs_layout = self.driver.find_element(By.CSS_SELECTOR,"div.up-card-section > div:nth-child(1) > div:nth-child(2)")
        html_data = jobs_layout.get_attribute('outerHTML')
        return html_data
    def parse_data(self, html_data):
        """
        
        
        """
        soup = BeautifulSoup(html_data, 'html.parser')
        job_list =soup.find_all('section', attrs={'data-test': 'JobTile'})
        jobs_data = {}
        for job in job_list:
            job_link = job.find('a')
            if not self.cache_db.cache_client.exists(job_link['href']): ## Caching the Jobs so we don't repeat the same job in message payload
                job_features = job.find('div' , attrs={'data-test': 'JobTileFeatures','class':'row'})
                jobs_data.update({job_link['href']:
                                    {'Features' : job_features.text , 'Title' : job_link.text}}
                                )
                self.cache_db.cache_client.set(job_link['href'],json.dumps({'Features' : job_features.text , 'Title' : job_link.text}) , ex = self.cache_db.ttl)
        return jobs_data

    def format_data(self,jobs_data):
        """
        
        
        
        
        """
        job_formatted_list = f"*Following are the new {self.query} jobs that have been posted* \n"
        for job_link in jobs_data: 
            title,features = jobs_data[job_link]['Title'],jobs_data[job_link]['Features']
            features = list(filter(lambda x: x != '', features.strip().
                                                      replace(':','').replace('\n','').
                                                      lower().split(' ')))
            job_formatted_list += f" - <https://www.upwork.com{job_link} | {title.strip()}> \n"
            
            # TODO Add features in a dictionary and make a final response by iterating over the items
            price = f'Hourly: {features[1]}' if 'hourly' in features else f'Fixed: {features[6]}'
            experience = f'Experience: {"-".join(features[-4:-2]).capitalize()}'\
                if 'entry' in features else f'Experience: {features[-3].capitalize()}' 
            posted = f'Posted: {" ".join(features[features.index("posted")+1:features.index("posted")+4])}'
            job_formatted_list += f"    - {price} \n"
            job_formatted_list += f"    - {experience} \n"
            job_formatted_list += f"    - {posted} \n"
        return job_formatted_list
