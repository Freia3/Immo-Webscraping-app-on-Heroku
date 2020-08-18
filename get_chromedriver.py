from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os

def get_chromedriver():
    if str(os.getcwd()) != "/app": #code executed on my local machine (windows)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("no-sandbox")
        driver = webdriver.Chrome(
            executable_path=str(os.getcwd())+"\chromedriver.exe", options=chrome_options)
        return driver
    else: #code executed on heroku container (unix)
        chrome_options = Options()
        chrome_options.binary_location = "/app/.apt/usr/bin/google-chrome"
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path="/app/.chromedriver/bin/chromedriver", options=chrome_options)
        return driver
