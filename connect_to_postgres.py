import psycopg2
import urllib.parse as urlparse
import os
from config import database_url


def connectToPostGresDB():
    if str(os.getcwd()) != "/app":  # code executed on my local machine (windows)
        url = urlparse.urlparse(database_url)
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
        con = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
    else:  # run from heroku
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
        con = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
    return con

