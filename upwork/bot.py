from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class Bot:
    def __init__(self,query):
        self.query = query
    def get_data(self):
        """
        
        
        """
        driver = webdriver.Chrome()
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
            jobs_data[job.find('a')['href']] = job.text
        return jobs_data