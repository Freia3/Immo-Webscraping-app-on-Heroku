from bs4 import BeautifulSoup
import requests
import time


def get_parsed_page_content(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        'referer': 'https://www.google.com/'} # referer added to avoid captcha on zimmo webpage

    r = requests.get(url, headers=headers)
    time.sleep(1)   # don't get blocked by requesting websource too fast after each other
    webpage = r.content.decode('utf8')
    soup = BeautifulSoup(webpage, 'html.parser')
    return soup
