from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from fake_headers import Headers

class UpworkBot:
    def __init__(self,query):
        self.query = query
    def get_data(self):
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
        jobs_layout = driver.find_element(By.CSS_SELECTOR,"div.up-card-section > div:nth-child(1) > div:nth-child(2)")
        html_data = jobs_layout.get_attribute('outerHTML')
        driver.quit()
        return html_data
    def parse_data(self, html_data):
        """
        
        
        """
        soup = BeautifulSoup(html_data, 'html.parser')
        job_list =soup.find_all('section', attrs={'data-test': 'JobTile'})
        jobs_data = {}
        for job in job_list:
            job_link = job.find('a')
            job_features = job.find('div' , attrs={'data-test': 'JobTileFeatures','class':'row'})
            jobs_data.update({job_link['href']:
                                {'Features' : job_features.text , 'Title' : job_link.text}}
                            )
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
