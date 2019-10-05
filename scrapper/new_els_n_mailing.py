#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, HtmlContent
from datetime import date
import os

allthatels_id = os.environ.get('ALLTHATELS_ID')
allthatels_pw = os.environ.get('ALLTHATELS_PW')

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920x1080')
options.add_argument('--disable-gpu')

today = date.today()
from_email = 'neocur@gmail.com', 'Paul Seo'
subject = 'New ELS list {0}'.format(today)
to_emails = [
    ('neocur@naver.com', 'Paul Seo')
]

def main():
    browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)
    browser.get('http://allthatels.co.kr/')

    browser.find_element_by_id('header_user_email').send_keys(allthatels_id)
    browser.find_element_by_id('header_user_pass').send_keys(allthatels_pw)
    browser.find_element_by_id('header_login_form').submit()
    browser.find_element_by_id('menu_els').click()

    browser.find_element_by_id('interest').send_keys('6')
    Select(browser.find_element_by_name('sortType')).select_by_value('연이율높은순')
    browser.find_element_by_id('submit_search').click()

    html = browser.page_source
    soup = BeautifulSoup(html , 'html.parser')
    els_table = soup.find('table', id='els_table')

    [x.extract() for x in els_table.find_all('img')]

    html_content = "<html>{0}</html>".format(els_table)
    html_content = html_content.replace('border="0"', 'border="1"', 1)

    browser.quit()
    #print(html_content)
    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content)

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message=message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

if __name__ == "__main__":
	main()
