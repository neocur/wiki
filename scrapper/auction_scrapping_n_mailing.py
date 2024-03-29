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

tankauct_id = os.environ.get('TANKAUCT_ID')
tankauct_pw = os.environ.get('TANKAUCT_PW')

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920x1080')
options.add_argument('--disable-gpu')

today = date.today()
from_email = 'neocur@gmail.com', 'Paul Seo'
subject = 'New auction list {0}'.format(today)
to_emails = [
    ('neocur@naver.com', 'Paul Seo'),
    ('neocur@daum.net', 'Hyun Seo')
]

def main():
    browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)
    #browser.implicitly_wait(3)

    browser.get('http://www.tankauction.co.kr/')

    element = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.ID, 'client_id'))
    )

    browser.find_element_by_id('client_id').send_keys(tankauct_id)
    browser.find_element_by_id('pwd_dummy').click()
    browser.find_element_by_id('passwd').send_keys(tankauct_pw)
    browser.find_element_by_id('passwd').submit()

    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, \
            "#wrap > div.login_box > div.fright > div > div.member_ment.right")))

    browser.find_element_by_xpath('//*[@id="wrap"]/div[1]/li[1]/a').click()
    browser.find_element_by_xpath('//*[@id="wrap"]/div[2]/ul/li[3]/a').click()
    browser.find_element_by_xpath('//*[@id="auct_addr"]/div[1]/ul/li[9]/a').click()
    browser.find_element_by_xpath('//*[@id="auct_addr"]/div[2]/table/tbody/tr[1]/td/ul/li[18]/a').click()

    Select(browser.find_element_by_name('state')).select_by_value('1')
    Select(browser.find_element_by_name('s_class')).select_by_value('1')
    browser.find_element_by_xpath('//*[@id="auct_addr"]/div[2]/table/tbody/tr[4]/td[4]/input[7]').click()
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'auct_list')))

    #browser.find_element_by_id('auct_list').screenshot('test.png')

    html = browser.page_source
    soup = BeautifulSoup(html , 'html.parser')
    #auct_table = soup.select('table.tbl_list')
    auct_table = soup.find(class_='tbl_list')

    html_content = "{0}".format(auct_table)

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

    browser.quit()

if __name__ == "__main__":
    main()
