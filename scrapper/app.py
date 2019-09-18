from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests, os

#application = Flask(__name__)
tankauct_id = os.environ.get('TANKAUCT_ID')
tankauct_pw = os.environ.get('TANKAUCT_PW')

#@application.route('/')
#def index_home():
#    return 'TEST!

browser = webdriver.Chrome('/usr/local/bin/chromedriver')
browser.implicitly_wait(3)

browser.get('http://www.tankauction.co.kr/')

browser.find_element_by_id('client_id').send_keys(tankauct_id)
browser.find_element_by_id('pwd_dummy').click()
browser.find_element_by_id('passwd').send_keys(tankauct_pw)
browser.find_element_by_id('passwd').submit()
browser.implicitly_wait(3)

browser.get('http://www.tankauction.co.kr/auction/ca_addr.php?sido=41&gugun=117&state=1,2,17,18')

Select(browser.find_element_by_name('state')).select_by_value('1')
Select(browser.find_element_by_name('s_class')).select_by_value('1')

browser.find_element_by_xpath('//*[@id="auct_addr"]/div[2]/table/tbody/tr[4]/td[4]/input[7]').click()

browser.implicitly_wait(3)
#browser.find_element_by_xpath('//*[@id="auct_list"]').screenshot_as_png('image.png')
#auct_list = browser.find_elements_by_tag_name('//*[@id="list_body"]/tr')
#browser.find_element_by_xpath('//*[@id="auct_list"]/table').screenshot_as_png('image.png')

auct_table = browser.find_elements_by_xpath('//*[@id="list_body"]/tr')

for auct_l in auct_table:
    print(auct_l.text)
    print('\n')

browser.close()

#if __name__ == '__main__':
#    application.run()