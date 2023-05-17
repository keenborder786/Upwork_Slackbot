from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

class UpworkBot:
    def __init__(self,query):
        self.query = query
    def get_data(self):
        """
        
        
        """
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1,1")
        driver = webdriver.Chrome(chrome_options = chrome_options)
        driver.get(f"https://www.upwork.com/nx/jobs/search/?q={self.query.replace(' ','%20')}&sort=recency")
        jobs_layout = driver.find_element(By.CSS_SELECTOR,"div.up-card-section > div:nth-child(1) > div:nth-child(2)")
        html_data = jobs_layout.get_attribute('outerHTML')
        driver.close()
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
            jobs_data[job_link['href']] = {'Title' : job_link.text}
            jobs_data[job_link['href']]['Features'] = job_features.text
        return jobs_data

    def format_data(self,jobs_data):
        """
        
        
        
        
        """
        job_formatted_list = f"*Following are the new {self.query} jobs that have been posted* \n"
        for job_link in jobs_data: 
            title,features = jobs_data[job_link]['Title'],jobs_data[job_link]['Features'].split('\n')
            other_meta_features = features[-1].strip().split(' ')
            job_formatted_list += f" - <https://www.upwork.com{job_link} | {title}> \n"
            if 'Fixed-price' in features[0].strip(): 
                posted_time = features[2].strip()
                price = f"{features[0].strip()}-{features[3].strip()}"
            else:
                posted_time = ' '.join(other_meta_features[:other_meta_features.index('ago')+1]) 
                price = features[0].strip()
            job_formatted_list += f"    - Price: {price} \n"
            job_formatted_list += f"    - Posted Time: {posted_time} \n"
        return job_formatted_list
