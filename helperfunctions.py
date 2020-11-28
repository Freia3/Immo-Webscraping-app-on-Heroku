import urllib.parse as urlparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from bs4 import BeautifulSoup
import requests
import time
import sys
import pandas as pd
from sqlalchemy import create_engine
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def connect_to_postgresdb(database_url):
    con = None
    if str(os.getcwd()) != "/app":  # code executed on my local machine (windows)
        url = urlparse.urlparse(database_url)
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
    else:  # run from heroku
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
    try:
        # connect to PostgreSQl database server
        con = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    return con


def fetch_records_psql(database_url):
    con=connect_to_postgresdb(database_url) #connect to PostGreSQL DB
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS public."Articles"(user_id serial PRIMARY KEY, article_id VARCHAR (150) NOT NULL);
        select article_id from public."Articles";""")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cur.close()
        return 1

    records = cur.fetchall()
    df=pd.DataFrame(records,columns=["article_id"])
    cur.close()
    con.close() #close connection to DB
    return df

def insert_into_psql(df_articles,database_url):
    engine = create_engine(database_url)
    df_articles.to_sql('Articles', engine, if_exists='append')

def get_chromedriver():
    if str(os.getcwd()) != "/app": #code executed on my local machine (windows)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("no-sandbox")
        # driver = webdriver.Chrome(
        #     executable_path=str(os.getcwd())+"\chromedriver.exe", options=chrome_options)
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
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


def get_parsed_page_content(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        'referer': 'https://www.google.com/'} # referer added to avoid captcha on zimmo webpage

    r = requests.get(url, headers=headers)
    time.sleep(1)   # don't get blocked by requesting websource too fast after each other
    webpage = r.content.decode('utf8')
    soup = BeautifulSoup(webpage, 'html.parser')
    return soup


def send_simple_message(list_articles, article_type, TO_EMAIL, MAILGUN_API_KEY,MAILGUN_DOMAIN, MYNAME):
    files_images = list_articles.get_list_files_images(article_type)
    html_message = list_articles.get_list_html_message(article_type)
    print(html_message)
    print(files_images)
    if html_message:  # if not empty
        return requests.post(
            "https://api.mailgun.net/v3/"+MAILGUN_DOMAIN+"/messages",
            auth=("api", MAILGUN_API_KEY),
            files=files_images,
            data={"from": MYNAME+"<mailgun@"+MAILGUN_DOMAIN+">",
                  "to": [TO_EMAIL],
                  "subject": f"{article_type}",
                  "html": html_message})
