from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup




QUERY = 'Python'
def get_data():
    """
    
    
    """
    driver = webdriver.Chrome()
    driver.get(f"https://www.upwork.com/nx/jobs/search/?q={QUERY.replace(' ','%20')}&sort=recency")
    jobs_layout = driver.find_element(By.CSS_SELECTOR,"div.up-card-section > div:nth-child(1) > div:nth-child(2)")
    html_data = jobs_layout.get_attribute('outerHTML')
    driver.close()
    return html_data

def parser_data(html_data):
    """
    
    
    """
    soup = BeautifulSoup(html_data, 'html.parser')
    job_list =soup.find_all('section', attrs={'data-test': 'JobTile'})
    jobs_data = {}
    for job in job_list:
        jobs_data[job.find('a')['href']] = job.text
    return jobs_data


html_data = get_data()
jobs_data = parser_data(html_data)