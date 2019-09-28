#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from bs4 import BeautifulSoup
from urllib import parse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, HtmlContent
from datetime import date
import os

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920x1080')
options.add_argument('--disable-gpu')

today = date.today()
from_email = 'neocur@gmail.com', 'Paul Seo'
subject = 'Upper circuit list {0}'.format(today)
to_emails = [
    ('neocur@naver.com', 'Paul Seo'),
    ('cys6130@gmail.com', 'Daniel Choi'),
    ('plashman@gmail.com', 'Harry Oh')
]

def get_news_link(stock):
    encoded_stock = parse.quote(stock)
    rss_query = parse.quote_plus('https://news.google.com/rss/search?q={0}%20when:1d&hl=ko&gl=KR&ceid=KR:ko'.format(encoded_stock))
    rss_link = 'https://rss.bloople.net/?url={0}&detail=-1&showtitle=false&type=html'.format(rss_query)
    #print(rss_query)
    #print(rss_link)
    return rss_link

def main():
    browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)
    browser.get('https://finance.naver.com/sise/sise_upper.nhn')

    html = browser.page_source

    browser.quit()

    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all(class_='box_type_l')
    out_html = ''

    for tb in tables:
        for link in tb.find_all('a'):
            if 'href' in link.attrs:
                new_link = get_news_link(link.text)
                link['href'] = new_link
        out_html += "{0}".format(tb)

    #print(out_html)
    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=out_html)

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
