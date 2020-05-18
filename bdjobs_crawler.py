import time
import pandas
import argparse
from datetime import datetime
from urllib.request import urlopen
from collections import defaultdict

from selenium import webdriver
from bs4 import BeautifulSoup as bs


def get_jobs(url):
    job_root_link = 'https://jobs.bdjobs.com/jobdetails.asp?id='
    first_page_html = urlopen(url).read()
    first_page_content = bs(first_page_html, 'html.parser')
    no_of_pages = len(first_page_content.find('div', class_='pagination').find_all('li')) - 1
    for i in range(1, no_of_pages + 1):
        browser = webdriver.Chrome(executable_path='chromedriver.exe')
        browser.get(url)
        if i == 1:
            # print(f'page{i}')
            doc_script = "return document.documentElement.outerHTML"
            time.sleep(20)
            html = browser.execute_script(doc_script)
            time.sleep(10)
            data = bs(html, 'html.parser')
        else:
            # print(f'page{i}')
            script = f"javascript:GoPage({i})"
            doc_script = "return document.documentElement.outerHTML"
            browser.execute_script(script)
            time.sleep(40)
            html = browser.execute_script(doc_script)
            time.sleep(10)
            data = bs(html, 'html.parser')
        job_deadlines = data.find_all('div', class_='dead-text-d')
        for deadline in job_deadlines:
            job_deadline = deadline.text.strip()
            if datetime.strptime(job_deadline, '%b %d, %Y') >= datetime.now():
                job_position = deadline.parent.parent.parent.parent.parent.parent.a.text.strip()
                required_experience = deadline.parent.parent.parent.div.get_text().strip()
                job_id = str(deadline.parent.parent.parent.parent.parent.parent.a.get('href').partition('id=')[-1])
                job_link = job_root_link + job_id.strip()
                # print(job_position, required_experience, job_deadline, job_link)
                data_dictionary['job_position'].append(job_position)
                data_dictionary['job_deadline'].append(job_deadline)
                data_dictionary['required_experience'].append(required_experience)
                data_dictionary['job_link'].append(job_link)
                browser.quit()
            else:
                browser.quit()
                continue
    filtered_jobs = pandas.DataFrame(dict(data_dictionary))
    filtered_jobs.to_csv('jobs.csv', sep=',', index=False)


if __name__ == "__main__":
    root_url = "https://jobs.bdjobs.com/jobsearch.asp?fcatId=8&icatId="
    data_dictionary = defaultdict(list)
    get_jobs(root_url)
