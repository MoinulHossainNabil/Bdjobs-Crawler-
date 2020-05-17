import json
import time
from datetime import datetime
from urllib.request import urlopen

from selenium import webdriver
from bs4 import BeautifulSoup as bs


def get_jobs(url):
    datetime_object = datetime.strptime('May 30, 2020', '%b %d, %Y')
    job_root_link = 'https://jobs.bdjobs.com/jobdetails.asp?id='
    for i in range(2, 4):
        print(f'page{i}')
        script = f"javascript:GoPage({i})"
        doc_script = "return document.documentElement.outerHTML"
        browser = webdriver.Chrome(executable_path='chromedriver.exe')
        browser.get(url)
        browser.execute_script(script)
        time.sleep(60)
        html = browser.execute_script(doc_script)
        time.sleep(10)
        data = bs(html, 'html.parser')
        no_of_pages = len(data.find('div', class_='pagination').find_all('li')) - 1
        job_deadline = data.find_all('div', class_='dead-text-d')
        jobs_and_link = {}
        for deadline in job_deadline:
            job_position = deadline.parent.parent.parent.parent.parent.parent.a.text.strip()
            required_experience = deadline.parent.parent.parent.div.get_text().strip()
            job_deadline = deadline.text.strip()
            job_id = str(deadline.parent.parent.parent.parent.parent.parent.a.get('href').partition('id=')[-1])
            job_link = job_root_link + job_id.strip()
            print(job_position, required_experience, job_deadline, job_link)
    

url = "https://jobs.bdjobs.com/jobsearch.asp?fcatId=8&icatId="
get_jobs(url)
